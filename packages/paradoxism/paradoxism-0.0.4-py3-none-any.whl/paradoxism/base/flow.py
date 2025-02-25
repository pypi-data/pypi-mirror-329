# paradoxism/flow.py
import json
import inspect
from functools import wraps
from typing import Callable, Any
import logging
import networkx as nx

from paradoxism.base.agent import _thread_local
from paradoxism.ops.ast import *

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class FlowExecutor:
    """負責執行流程並管理流程狀態的類別。"""

    def __init__(self, max_retries: int = 3, max_steps: int = 100):
        self.max_retries = max_retries
        self.max_steps = max_steps
        self.state = {}
        self.outputs = {}
        self.current_step = 0
        self.visited = {}  # 記錄每個步驟的執行次數
        self.step_calls = []  # 記錄步驟的執行順序

        # Initialize a directed graph
        self.graph = nx.DiGraph()

    def execute_agent(self, agent_func: Callable, *args, **kwargs) -> Any:
        """執行單個 agent 函數，並管理重試和狀態。"""
        agent_name = agent_func.__name__
        step_name = f"{agent_name}_{self.current_step + 1}"

        if self.current_step >= self.max_steps:
            logger.error("達到最大執行步驟數。可能存在無窮迴圈。")
            raise RuntimeError("達到最大執行步驟數。可能存在無窮迴圈。")

        if step_name in self.visited:
            self.visited[step_name] += 1
            if self.visited[step_name] > self.max_retries:
                logger.error(f"步驟 '{step_name}' 超過最大重試次數。流程中斷。")
                raise RuntimeError(f"步驟 '{step_name}' 超過最大重試次數。")
        else:
            self.visited[step_name] = 1

        retries = 0
        while retries < self.max_retries:
            try:
                logger.info(f"執行 步驟: {step_name}")
                # 如果是 @agent 函數，設置 thread-local 的 llm_client
                if hasattr(agent_func, 'llm_client'):
                    _thread_local.llm_client = agent_func.llm_client
                else:
                    _thread_local.llm_client = None

                output = agent_func(*args, **kwargs)
                self.outputs[step_name] = output
                self.state[step_name] = 'completed'
                logger.info(f"步驟 '{step_name}' 完成，輸出: {output}")
                break
            except Exception as e:
                retries += 1
                logger.error(f"執行步驟 '{step_name}' 時發生錯誤: {e}. 重試 {retries}/{self.max_retries}")
                self.state[step_name] = 'retrying'
            finally:
                # 清除 thread-local 中的 llm_client
                _thread_local.llm_client = None
        else:
            logger.error(f"步驟 '{step_name}' 在重試 {self.max_retries} 次後仍失敗。")
            self.state[step_name] = 'failed'
            raise RuntimeError(f"步驟 '{step_name}' 在重試 {self.max_retries} 次後仍失敗。")

        # 記錄步驟的調用順序並添加到圖中
        self.step_calls.append(step_name)
        if len(self.step_calls) > 1:
            self.graph.add_edge(self.step_calls[-2], step_name)
        else:
            self.graph.add_node(step_name)

        self.current_step += 1
        return self.outputs[step_name]

    def to_mermaid(self) -> str:
        """從有向圖生成 Mermaid 流程圖字符串。"""
        mermaid = "graph TD\n"
        for edge in self.graph.edges:
            mermaid += f"    {edge[0]} --> {edge[1]}\n"
        # 添加獨立節點
        for node in self.graph.nodes:
            if self.graph.in_degree(node) == 0 and self.graph.out_degree(node) == 0:
                mermaid += f"    {node}\n"
        return mermaid

    def save_outputs(self, filename: str = "flow_outputs.json"):
        """將流程的輸出結果保存為 JSON 文件。"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.outputs, f, ensure_ascii=False, indent=4)
        logger.info(f"流程輸出已保存至 {filename}")

def flow():
    """
    @flow 裝飾器，用於定義和執行一個流程。
    """
    def decorator(flow_func: Callable):
        @wraps(flow_func)
        def wrapper(*args, **kwargs):
            executor = FlowExecutor()
            parser=CodeFlowParser()
            code=inspect.getsource(flow_func)
            flow_result = parser.parse(code)
            dependencies_list, step_details = generate_dependency_list_from_flow(flow_result)
            # 建立有向圖
            G = nx.DiGraph()

            # 根據依賴關係新增節點和有向邊
            for dep in dependencies_list:
                G.add_edge(dep['from'], dep['to'])
            # 檢查是否有循環
            cycle = handle_cycles(G)

            # 執行拓撲排序並分層
            parallelizable_layers = topological_sort_with_levels(G)

            # 輸出每層可以併行執行的步驟
            for i, layer in enumerate(parallelizable_layers):
                print(f"Layer {i + 1}: {layer}")

            # 設置當前線程的 executor
            _thread_local.executor = executor
            _thread_local.flow_parser=parser
            _thread_local.code=code
            _thread_local.flow_result = flow_result
            _thread_local.dependencies_list=dependencies_list
            _thread_local.step_details = step_details

            try:
                # 執行流程函數，並將 executor 作為第一個參數
                flow_func(executor, *args, **kwargs)
            except Exception as e:
                logger.error(f"流程執行失敗: {e}")
            finally:
                # 移除線程中的 executor
                del _thread_local.executor
            # 生成 Mermaid 流程圖
            mermaid = generate_mermaid_from_flow(flow_result)
            logger.info(f"Mermaid 流程圖:\n{mermaid}")
            # 保存輸出結果
            executor.save_outputs()
            # 返回流程執行的所有輸出
            return executor.outputs
        return wrapper
    return decorator