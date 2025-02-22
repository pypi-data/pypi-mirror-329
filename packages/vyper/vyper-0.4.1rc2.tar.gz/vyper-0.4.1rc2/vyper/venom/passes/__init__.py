from .algebraic_optimization import AlgebraicOptimizationPass
from .branch_optimization import BranchOptimizationPass
from .dft import DFTPass
from .float_allocas import FloatAllocas
from .function_inliner import FunctionInlinerPass
from .literals_codesize import ReduceLiteralsCodesize
from .load_elimination import LoadElimination
from .lower_dload import LowerDloadPass
from .make_ssa import MakeSSA
from .mem2var import Mem2Var
from .memmerging import MemMergePass
from .normalization import NormalizationPass
from .remove_unused_variables import RemoveUnusedVariablesPass
from .sccp import SCCP
from .simplify_cfg import SimplifyCFGPass
from .store_elimination import StoreElimination
from .store_expansion import StoreExpansionPass
