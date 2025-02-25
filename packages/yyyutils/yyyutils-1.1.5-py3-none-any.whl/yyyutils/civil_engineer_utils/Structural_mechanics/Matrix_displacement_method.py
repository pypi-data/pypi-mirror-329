"""
注意事项：
1. 确定某方向位移为0时，编号时设置为0，但不ignore这个方向（ignore代表忽略相关所有位移和所有力）
2. 确定某方向力为0时，使用set_zeros_（）参数，但是不ignore这个力所在的方向
3. Kx的大小等于有效位移编号的最大值
4. 最后求出的F和FD大小相同，FD的大小取决于是否忽略某种力，不忽略的情况，FD大小为6*1（i端和j端）
"""
import sympy as sp
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve, lsqr
import contextlib
import io
import sys
from yyyutils.print_utils import PrintUtils

pr = PrintUtils(add_line=False, flush=True)
op = PrintUtils.original_print


class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()


class DefineSymbols:
    """
    定义符号变量
    """

    def __init__(self):
        # 定义支持的符号变量
        self.EA, self.EA1, self.EA2, self.EA3, self.EI, self.EI1, self.EI2, self.EI3 = sp.symbols(
            'EA EA1 EA2 EA3 EI EI1 EI2 EI3')
        self.L, self.L1, self.L2, self.L3, self.alpha, self.alpha1, self.alpha2, self.alpha3, self.alpha4, self.alpha5, self.alpha6 = sp.symbols(
            'L L1 L2 L3 alpha alpha1 alpha2 alpha3 alpha4 alpha5 alpha6')
        self.F, self.F1, self.F2, self.F3, self.F4, self.F5, self.F6, self.a, self.b, self.a1, self.b1, self.a2, self.b2, self.a3, self.b3, self.a4, self.b4, self.a5, self.b5, self.a6, self.b6 = sp.symbols(
            'F F1 F2 F3 F4 F5 F6 a b a1 b1 a2 b2 a3 b3 a4 b4 a5 b5 a6 b6')
        self.q, self.l, self.q2, self.l2, self.q1, self.l1, self.q3, self.l3, self.q4, self.l4, self.q5, self.l5, self.q6, self.l6 = sp.symbols(
            'q l q2 l2 q1 l1 q3 l3 q4 l4 q5 l5 q6 l6')
        self.delta, self.delta1, self.delta2, self.delta3, self.delta4, self.delta5, self.delta6 = sp.symbols(
            'delta delta1 delta2 delta3 delta4 delta5 delta6')
        self.i, self.i1, self.i2, self.i3, self.i4, self.i5, self.i6 = sp.symbols('i i1 i2 i3 i4 i5 i6')
        self.FD, self.FD1, self.FD2, self.FD3, self.FD4, self.FD5, self.FD6 = sp.symbols('FD FD1 FD2 FD3 FD4 FD5 FD6')
        self.subs_token = False

    def set_symbols_subs(self, subs_dict):
        """
        设置符号变量的替换字典
        """
        # 更新实例变量
        self.subs_token = True
        self.__dict__.update({str(key): value for key, value in subs_dict.items()})


class MatrixDisplacementMethodUtils(DefineSymbols):
    """
    矩阵位移法工具类
    """

    def __init__(self):
        super(MatrixDisplacementMethodUtils, self).__init__()
        self.output_buffer = io.StringIO()
        # 定义常量
        self.PI = sp.pi
        self.INF = 1e20

    def expand_matrix_(self, matrix):
        """
        展开矩阵，在每个元素的右侧和下方补零。

        参数:
        matrix (sympy.Matrix): 输入的矩阵。

        返回:
        sympy.Matrix: 扩展后的矩阵。
        """
        # 获取原始矩阵的行数和列数
        rows, cols = matrix.shape

        # 创建一个大小为 (2*rows, 2*cols) 的零矩阵
        expanded_matrix = sp.zeros(rows * 2, cols * 2)

        # 将原矩阵的元素放入新矩阵的适当位置
        for i in range(rows):
            for j in range(cols):
                expanded_matrix[i * 2, j * 2] = matrix[i, j]

        return expanded_matrix

    def colculate_k_e_(self, unit_num, unit_le, unit_EA, unit_EI, set_zeros_FN=False, set_zeros_Fs=False,
                       set_zeros_M=False,
                       ignore_x=False, ignore_y=False, ignore_beta=False,
                       expand_matrix=False, reverse_M=False):
        """
        计算单元的局部坐标系下的刚度矩阵
        """
        all_k_e = []
        for i in range(unit_num):
            k_e = sp.Matrix([
                [unit_EA[i] / unit_le[i], 0, 0, -unit_EA[i] / unit_le[i], 0, 0],
                [0, 12 * unit_EI[i] / unit_le[i] ** 3, 6 * unit_EI[i] / unit_le[i] ** 2, 0,
                 -12 * unit_EI[i] / unit_le[i] ** 3,
                 6 * unit_EI[i] / unit_le[i] ** 2],
                [0, 6 * unit_EI[i] / unit_le[i] ** 2, 4 * unit_EI[i] / unit_le[i], 0, -6 * unit_EI[i] / unit_le[i] ** 2,
                 2 * unit_EI[i] / unit_le[i]],
                [-unit_EA[i] / unit_le[i], 0, 0, unit_EA[i] / unit_le[i], 0, 0],
                [0, -12 * unit_EI[i] / unit_le[i] ** 3, -6 * unit_EI[i] / unit_le[i] ** 2, 0,
                 12 * unit_EI[i] / unit_le[i] ** 3,
                 -6 * unit_EI[i] / unit_le[i] ** 2],
                [0, 6 * unit_EI[i] / unit_le[i] ** 2, 2 * unit_EI[i] / unit_le[i], 0, -6 * unit_EI[i] / unit_le[i] ** 2,
                 4 * unit_EI[i] / unit_le[i]],
            ])
            # 处理特殊情况
            if reverse_M:
                k_e[2, :] = -k_e[2, :]  # 反转M
                k_e[5, :] = -k_e[5, :]  # 反转M
            zero_row = sp.zeros(1, 6)
            if set_zeros_FN:
                # 第一行和第四行置零
                k_e[0, :] = zero_row
                k_e[3, :] = zero_row
            if set_zeros_Fs:
                k_e[1, :] = zero_row
                k_e[4, :] = zero_row
            if set_zeros_M:
                k_e[2, :] = zero_row
                k_e[5, :] = zero_row
            del_idx = []
            if ignore_x:
                del_idx.append(0)  # 第一行和第一列
                del_idx.append(3)
            if ignore_y:
                del_idx.append(1)
                del_idx.append(4)  # 第二行和第二列
            if ignore_beta:
                del_idx.append(2)  # 第三行和第三列
                del_idx.append(5)

            # 从原矩阵中提取剩下的行和列，形成新的矩阵
            need_idx = list(set(range(6)) - set(del_idx))
            k_e = k_e.extract(need_idx, need_idx)
            # if expand_matrix:
            #     k_e = expand_matrix_(k_e)

            all_k_e.append(k_e)
            try:
                print(f"单元{i + 1}局部刚度矩阵为：\n{np.array(k_e).astype(float)}")
            except:
                print(f"单元{i + 1}局部刚度矩阵为：\n{np.array(k_e)}")
        return all_k_e

    def colculate_Te(self, unit_num, alphas, ignore_x=False, ignore_y=False, ignore_beta=False, expand_matrix=False):
        """
        计算转换矩阵
        """
        all_Te = []
        for i in range(unit_num):
            Te = sp.Matrix([
                [sp.cos(alphas[i]), sp.sin(alphas[i]), 0, 0, 0, 0],
                [-sp.sin(alphas[i]), sp.cos(alphas[i]), 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0],
                [0, 0, 0, sp.cos(alphas[i]), sp.sin(alphas[i]), 0],
                [0, 0, 0, -sp.sin(alphas[i]), sp.cos(alphas[i]), 0],
                [0, 0, 0, 0, 0, 1]
            ])
            del_idx = []
            if ignore_x:
                del_idx.append(0)  # 第一行和第一列
                del_idx.append(3)
            if ignore_y and not expand_matrix:
                del_idx.append(1)
                del_idx.append(4)  # 第二行和第二列
            if ignore_beta:
                del_idx.append(2)  # 第三行和第三列
                del_idx.append(5)
            need_idx = list(set(range(6)) - set(del_idx))
            Te = Te.extract(need_idx, need_idx)
            all_Te.append(Te)
            try:
                print(f"单元{i + 1}的转换矩阵为：\n{np.array(Te).astype(float)}")
            except:
                print(f"单元{i + 1}的转换矩阵为：\n{np.array(Te)}")
        return all_Te

    def colculate_ke(self, all_k_e, all_Te):
        """
        计算全局单元刚度矩阵
        """
        all_ke = []
        for i in range(len(all_k_e)):
            ke = all_Te[i].T * all_k_e[i] * all_Te[i]
            all_ke.append(ke)
            try:
                print(f"单元{i + 1}全局刚度矩阵为：\n{np.array(ke).astype(float)}")
            except:
                print(f"单元{i + 1}全局刚度矩阵为：\n{np.array(ke)}")
        return all_ke

    def generate_lambda(self, all_lambda_str):
        """
        生成λ指示矩阵
        """
        from yyyutils.data_structure_utils import StringUtils
        all_lambda_matrix = sp.Matrix(StringUtils.transform_input_to_t_list(all_lambda_str, " ", ","))
        try:
            print(f"所有单元的定位向量为：\n{np.array(all_lambda_matrix).astype(int)}")
        except:
            print(f"所有单元的定位向量为：\n{np.array(all_lambda_matrix)}")
        return all_lambda_matrix

    def colculate_kx(self, all_ke, all_lambda):
        """
        计算全局结构刚度矩阵
        """
        # 找到all_lambda中的最大值存入size
        size = int(self.numeric_matrix_max(all_lambda))
        kx = sp.zeros(size, size)
        for i in range(1, kx.shape[0] + 1):
            for j in range(1, kx.shape[1] + 1):
                for k in range(len(all_ke)):
                    lambda_k = all_lambda[k, :]
                    kei = [idx for idx, val in enumerate(lambda_k) if val == i]
                    kej = [idx for idx, val in enumerate(lambda_k) if val == j]
                    if kei and kej:
                        for l in range(len(kei)):
                            for m in range(len(kej)):
                                kx[i - 1, j - 1] += all_ke[k][kei[l], kej[m]]
        try:
            print(f"全局结构刚度矩阵为：\n{np.array(kx).astype(float)}")
        except:
            print(f"全局结构刚度矩阵为：\n{np.array(kx)}")
        return kx

    def colculate_F_Fe(self, unit_num, Fs, qs, deltas, Ls, cetas, ignore_x=False, ignore_y=False, ignore_beta=False,
                       expand_matrix=False,
                       reverse_M=False):
        """
        计算各单元在局部坐标系下的固端力
        """
        all_F_Fe = []
        for i in range(unit_num):
            F = Fs[i]
            q = qs[i]
            delta = list(deltas[i])
            if len(delta) == 2:
                delta.append(self.i)
            delta.append(Ls[i])

            # ceta = cetas[i]

            Fsi1 = Mi1 = Fsj1 = Mj1 = Fsi2 = Mi2 = Fsj2 = Mj2 = Fsi3 = Mi3 = Fsj3 = Mj3 = sp.S(0)
            if F is not None:
                Fsi1 = -F[0] * F[2] ** 2 * (3 * F[1] + F[2]) / (F[1] + F[2]) ** 3
                Mi1 = -F[0] * F[1] * F[2] ** 2 / (F[1] + F[2]) ** 2
                Fsj1 = -F[0] * F[1] ** 2 * (F[1] + 3 * F[2]) / (F[1] + F[2]) ** 3
                Mj1 = F[0] * F[1] ** 2 * F[2] / (F[1] + F[2]) ** 2
            if q is not None:
                Fsi2 = -q[0] * q[1] / (2 * q[2] ** 3) * (2 * q[2] ** 3 - 2 * q[2] * q[1] ** 2 + q[1] ** 3)
                Mi2 = -q[0] * q[1] ** 2 / (12 * q[2] ** 2) * (6 * q[2] ** 2 - 8 * q[2] * q[1] + 3 * q[1] ** 2)
                Fsj2 = -q[0] * q[1] ** 3 / (2 * q[2] ** 3) * (2 * q[2] - q[1])
                Mj2 = q[0] * q[1] ** 3 / (12 * q[2] ** 2) * (4 * q[2] - 3 * q[1])
            if delta is not None:
                right_delta = delta[1] - delta[0]
                Fsi3 = 12 * delta[2] / delta[3] * right_delta
                Mi3 = 6 * delta[2] / delta[3] * right_delta
                Fsj3 = -12 * delta[1] / delta[3] * right_delta
                Mj3 = 6 * delta[2] / delta[3] * right_delta
            if reverse_M:
                Mi1, Mj1, Mi2, Mj2, Mi3, Mj3 = -Mi1, -Mj1, -Mi2, -Mj2, -Mi3, -Mj3
            F_Fe = sp.Matrix([0, Fsi1 + Fsi2 + Fsi3, Mi1 + Mi2 + Mi3, 0, Fsj1 + Fsj2 + Fsj3, Mj1 + Mj2 + Mj3])

            del_idx = []
            if ignore_x:
                del_idx.append(0)
                del_idx.append(3)
            if ignore_y and not expand_matrix:
                del_idx.append(1)
                del_idx.append(4)
            if ignore_beta:
                del_idx.append(2)
                del_idx.append(5)
            need_idx = list(set(range(6)) - set(del_idx))
            F_Fe = F_Fe.extract(need_idx, [0])
            all_F_Fe.append(F_Fe)
            try:
                print(f"单元{i + 1}的局部固端力为：\n{np.array(F_Fe).astype(float)}")
            except:
                print(f"单元{i + 1}的局部固端力为：\n{np.array(F_Fe)}")
        return all_F_Fe

    def colculate_FFe(self, all_F_Fe, all_Te):
        """
        计算单元全局固端力
        """
        all_FFe = []
        for i in range(len(all_Te)):
            FFe = all_Te[i].T * all_F_Fe[i]

            all_FFe.append(FFe)
            try:
                print(f"单元{i + 1}的全局固端力为：\n{np.array(FFe).astype(float)}")
            except:
                print(f"单元{i + 1}的全局固端力为：\n{np.array(FFe)}")
        return all_FFe

    def coculate_FE(self, all_FFe, all_lambda):
        """
        计算等效节点荷载
        """
        non_zero_elements = [x for x in all_lambda if x != 0]
        unique_non_zero_elements = sorted(set(non_zero_elements))
        print(f"所有节点非0编号为：\n{np.array(unique_non_zero_elements)}")
        FE = sp.zeros(len(unique_non_zero_elements), 1)
        for i in range(1, len(unique_non_zero_elements) + 1):
            for j in range(all_lambda.shape[0]):
                k = [idx for idx, val in enumerate(all_lambda[j, :]) if val == i]
                if k:
                    FE[i - 1] += all_FFe[j][k[0]]
        FE = -FE
        try:
            print(f"等效节点荷载为：\n{np.array(FE).astype(float)}")
        except:
            print(f"等效节点荷载为：\n{np.array(FE)}")
        return FE

    def coculate_F(self, FE, FD):
        """
        计算各节点的综合节点荷载
        """
        F = FE + FD
        try:
            print(f"各节点综合节点荷载为：\n{np.array(F).astype(float)}")
        except:
            print(f"各节点综合节点荷载为：\n{np.array(F)}")
        return F

    def solve_equation(self, K, F):
        if isinstance(K, sp.Matrix) or isinstance(F, sp.Matrix) or any(
                isinstance(elem, sp.Expr) for elem in K.flat) or any(
            isinstance(elem, sp.Expr) for elem in F.flat):
            return self.solve_symbolic(K, F)
        else:
            return self.solve_numeric(K, F)

    def solve_symbolic(self, K, F):
        K = sp.Matrix(K)
        F = sp.Matrix(F)

        try:
            # 尝试使用 SymPy 的线性方程求解器
            X = K.solve(F)
        except sp.matrices.exceptions.NonInvertibleMatrixError:
            # 如果矩阵奇异，尝试使用广义逆（Moore-Penrose 伪逆）
            K_pinv = K.pinv()
            X = K_pinv * F
            print("警告：矩阵奇异，使用广义逆求解。结果可能不是唯一解。")

        return X

    def solve_numeric(self, K, F):
        K = np.array(K, dtype=float)
        F = np.array(F, dtype=float).ravel()

        K_sparse = sparse.csc_matrix(K)

        try:
            # 尝试使用 spsolve
            X = spsolve(K_sparse, F)
        except sparse.linalg.MatrixRankWarning:
            # 如果 spsolve 失败，使用最小二乘法求解
            X, _, _, _ = lsqr(K_sparse, F)[:4]
            print("警告：矩阵可能奇异，使用最小二乘法求解。结果可能不是唯一解。")

        return X

    def calculate_delta(self, F, kx):
        """
        计算位移
        """
        print("开始计算位移")
        delta = self.solve_equation(kx, F)
        try:
            print(f"各节点位移为：\n{np.array(delta).astype(float)}")
        except:
            print(f"各节点位移为：\n{np.array(delta)}")
        return delta

    def coculate_F_(self, all_F_Fe, all_Te, all_ke, X, all_lambda, reverse_M=False):
        """
        计算各单元杆端力
        """
        all_F_ = []
        for i in range(len(all_F_Fe)):
            lambda_i = all_lambda[i, :]
            res = sp.zeros(len(lambda_i), 1)
            for j in range(len(lambda_i)):
                if lambda_i[j] != 0:
                    res[j] = X[lambda_i[j] - 1]
            F_ = all_F_Fe[i] + all_Te[i] * all_ke[i] * res
            # if reverse_M:
            #     print("警告：使用reverse_M选项，只能保证局部坐标系下的杆端力的正确性，前面的结果可能不准确。")
            #     temp = F_.shape[0] // 2
            #     F_[temp - 1, :] = -F_[temp - 1, :]
            #     F_[2 * temp - 1, :] = -F_[2 * temp - 1, :]

            all_F_.append(F_)
            try:
                print(f"单元{i + 1}的杆端力为：\n{np.array(F_).astype(float)}")
            except:
                print(f"单元{i + 1}的杆端力为：\n{np.array(F_)}")
        return all_F_

    def numeric_matrix_max(self, matrix):
        return np.max(np.array(matrix.tolist()).astype(float))

    def generate_by_none_or_all_or_singleelement_or_oneplusother(self, obj, unit_num, defualt):
        if obj is None:
            U_obj = [defualt] * unit_num
        elif isinstance(obj, list):
            if len(obj) == 1 or not isinstance(obj[1], list):
                U_obj = obj
            else:
                U_obj = [obj[0]] * unit_num
                for item in obj[1]:
                    U_obj[item[0] - 1] = item[1]
        else:
            U_obj = [obj] * unit_num
        return U_obj

    def generate_by_none_or_all_or_specialelements(self, obj, unit_num):
        U_obj = [None] * unit_num
        if obj is not None:
            if not isinstance(obj, list):
                raise ValueError("Fs参数输入有误，请检查。")
            elif obj[0] is None or not isinstance(obj[0][1], tuple):
                U_obj = obj
            else:
                for i in range(len(obj)):
                    U_obj[obj[i][0] - 1] = obj[i][1]
        return U_obj

    def run(self, all_lambda_str, unit_num, unit_le=None, unit_EA=None, unit_EI=None, alphas=None, FD=None, Fs=None,
            qs=None,
            deltas=None, cetas=None,
            set_zeros_FN=False,
            set_zeros_Fs=False,
            set_zeros_M=False,
            ignore_x=False,
            ignore_y=False,
            ignore_beta=False,
            expand_matrix=False,
            coculate_X_F_forced=False, reverse_M=False):
        """
        主函数
        :param unit_num: 单元数量
        :param unit_le: 单元长度参数，传入形式：[unit_length，[(unit_id, unit_length),...]]
        :param unit_EA: 单元EA参数，传入形式：[EA, [(unit_id, EA),...]]
        :param unit_EI: 单元EI参数，传入形式：[EI, [(unit_id, EI),...]]
        :param alphas: 单元与X轴夹角参数，传入形式：[alpha1, alpha2, alpha3,...]
        :param all_lambda_str: 指示矩阵的字符串形式（编号）
        :param subs_token: 是否已经替换符号变量
        :param FD: 节点在全局坐标系下的直接荷载参数，以与全局坐标系方向相同为正，传入形式：[(node_id, load), (node_id, load),...]
        :param Fs: 单元集中力参数，以与局部坐标系方向相同为正，传入形式：[(node_id, (F1, a1, b1)), (node_id, (F2, a2, b2)),...]
        :param qs: 单元均布荷载参数，以与局部坐标系方向相同为正，传入形式：[(node_id, (q1, l1, L1)), (node_id, (q2, l2, L2)),...]
        :param deltas: 支座位移参数，以支座向下位移为正，传入形式：[(node_id, (delta_left1, delta_right1, i1, L1), (delta_left2, delta_right2, i2, L2)),...]
        :param sub_dict: 符号变量替换字典
        :param set_zeros_FN: 是否不考虑轴力（注意，此项不决定是否不考虑x方向位移）
        :param set_zeros_Fs: 是否不考虑剪力（注意，此项不决定是否不考虑y方向位移）
        :param set_zeros_M: 是否不考虑弯矩（注意，此项不决定是否不考虑β方向转角）
        :param ignore_x: 是否忽略轴力和及其方向的位移
        :param ignore_y: 是否忽略剪力和及其方向的位移
        :param ignore_beta: 是否忽略弯矩和及其方向的转角
        :param expand_matrix:
        :return:
        """
        with contextlib.redirect_stdout(Tee(sys.stdout, self.output_buffer)):
            U_EA = self.generate_by_none_or_all_or_singleelement_or_oneplusother(unit_EA, unit_num, self.EA)
            U_EI = self.generate_by_none_or_all_or_singleelement_or_oneplusother(unit_EI, unit_num, self.EI)
            U_L = self.generate_by_none_or_all_or_singleelement_or_oneplusother(unit_le, unit_num, self.L)
            U_alphas = self.generate_by_none_or_all_or_singleelement_or_oneplusother(alphas, unit_num, self.alpha)
            print(f"节点位移编号字符串为：{all_lambda_str}")
            all_lambda_matrix = self.generate_lambda(all_lambda_str)
            U_FD = sp.zeros(int(self.numeric_matrix_max(all_lambda_matrix)), 1)
            if FD is not None:
                if not isinstance(FD, list):
                    raise ValueError("FD参数输入有误，请检查。")
                elif not isinstance(FD[0], tuple):
                    U_FD = sp.Matrix(FD)
                else:
                    for item in FD:
                        U_FD[item[0] - 1] = item[1]

            U_cetas = [None] * unit_num

            U_Fs = self.generate_by_none_or_all_or_specialelements(Fs, unit_num)
            U_qs = self.generate_by_none_or_all_or_specialelements(qs, unit_num)
            U_deltas = self.generate_by_none_or_all_or_specialelements(deltas, unit_num)

            print(f"单元长度参数为：{U_L}")
            print(f"单元EA参数为：{U_EA}")
            print(f"单元EI参数为：{U_EI}")
            print(f"单元与X轴夹角参数为：{U_alphas}")
            print(f"单元集中力参数为：{U_Fs}")
            print(f"单元均布荷载参数为：{U_qs}")
            print(f"支座位移参数为：{U_deltas}")

            print(f"节点直接荷载参数为：{U_FD}")

            print()
            all_k_e = self.colculate_k_e_(unit_num, U_L, U_EA, U_EI, set_zeros_FN, set_zeros_Fs, set_zeros_M, ignore_x,
                                          ignore_y,
                                          ignore_beta, expand_matrix, reverse_M)
            all_Te = self.colculate_Te(unit_num, U_alphas, ignore_x, ignore_y, ignore_beta, expand_matrix)
            all_ke = self.colculate_ke(all_k_e, all_Te)
            kx = self.colculate_kx(all_ke, all_lambda_matrix)
            all_F_Fe = self.colculate_F_Fe(unit_num, U_Fs, U_qs, U_deltas, U_L, U_cetas, ignore_x, ignore_y,
                                           ignore_beta,
                                           expand_matrix,
                                           reverse_M)  # 以单元为计算单位
            all_FFe = self.colculate_FFe(all_F_Fe, all_Te)
            FE = self.coculate_FE(all_FFe, all_lambda_matrix)  # 以节点为计算单位
            F = self.coculate_F(FE, U_FD)  # 以杆为计算单位
            if self.subs_token:
                X = self.calculate_delta(F, kx)  # 使用新的函数名
                if X is not None:
                    all_F_ = self.coculate_F_(all_F_Fe, all_Te, all_ke, X, all_lambda_matrix)
                else:
                    print("无法计算杆端力，因为位移计算失败。")
            else:
                if coculate_X_F_forced:
                    X = self.calculate_delta(F, kx)  # 使用新的函数名
                    if X is not None:
                        all_F_ = self.coculate_F_(all_F_Fe, all_Te, all_ke, X, all_lambda_matrix)
                    else:
                        print("无法计算杆端力，因为位移计算失败。")
                else:
                    print("由于没有替换符号变量，无法计算各节点位移和杆端力。")

            print()
        output = self.output_buffer.getvalue()
        print(output)

        save_to_file = input("是否保存结果到output.txt文件？（y/n）")
        if save_to_file.lower() == 'y':
            prompt = input("请输入本次实验的名称或描述：")
            with open('output.txt', 'a', encoding='GBK') as f:
                f.write(f"{prompt}\n")
                f.write(output)
            print("结果已保存到output.txt文件。")
        else:
            print("结果未保存。")

    # def subs_(self, subs_dict):
    #     """
    #     对字典里的所有符号变量进行替换
    #     :param subs_dict: 包含符号变量及其值的字典
    #     :return: 替换后的字典
    #     """
    #     global subs_token
    #
    #     updated = True
    #     while updated:
    #         updated = False
    #         for key, value in subs_dict.items():
    #             if isinstance(value, sp.Expr):
    #                 new_value = value.subs(subs_dict)
    #                 if new_value != value:
    #                     subs_dict[key] = new_value
    #                     updated = True

    # # 更新全局变量
    # globals().update({str(key): value for key, value in subs_dict.items()})
    # self.subs_token = True


"""
example:
utils = MatrixDisplacementMethodUtils()
    all_lambda_str = '0,1 1,2 2,3 3,4'
    subs_dict = {
    }
    utils.set_symbols_subs(subs_dict)
    utils.run(
        unit_num=4,
        alphas=0,
        deltas=[(0, utils.delta / 2), (utils.delta / 2, utils.delta, 2 * utils.i), (utils.delta, utils.delta / 2),
                (utils.delta / 2, 0, 2 * utils.i)],
        all_lambda_str=all_lambda_str,
        ignore_x=True,
        ignore_y=True,
        coculate_X_F_forced=True,
    )
"""

if __name__ == '__main__':
    utils = MatrixDisplacementMethodUtils()
    all_lambda_str = '0,1 1,2 2,3 3,4'
    subs_dict = {
    }
    utils.set_symbols_subs(subs_dict)
    utils.run(
        unit_num=4,
        alphas=0,
        deltas=[(0, utils.delta / 2), (utils.delta / 2, utils.delta, 2 * utils.i), (utils.delta, utils.delta / 2),
                (utils.delta / 2, 0, 2 * utils.i)],
        all_lambda_str=all_lambda_str,
        ignore_x=True,
        ignore_y=True,
        coculate_X_F_forced=True,
    )

    """
    TODO:
    1. 增加对转角引起的固端力的支持
    2. 增加弯矩引起的固端力的支持
    3. 当正方向不同时，考虑将全局正方向变成与局部正方向相同（现在采用的是将局部正方向变成与全局正方向相同）
    4. 用先处理法求出全局单刚之后，输出一个后处理法的原始刚度矩阵
    """
