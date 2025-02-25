# from qiskit import QuantumCircuit, transpile
# from qiskit_aer import Aer
# import matplotlib.pyplot as plt
#
#
# #
# # # 创建一个量子电路，包含1个量子比特和1个经典比特
# # circuit = QuantumCircuit(1, 1)
# #
# # # 应用Hadamard门，创建叠加态
# # circuit.h(0)
# #
# # # 测量量子比特并将结果保存到经典比特
# # circuit.measure(0, 0)
# #
# # # 使用Aer's qasm_simulator模拟器执行量子电路
# # simulator = Aer.get_backend('qasm_simulator')
# #
# # # 编译电路
# # transpiled_circuit = transpile(circuit, simulator)
# #
# # # 运行电路并获取结果
# # result = simulator.run(transpiled_circuit, shots=1000).result()
# #
# # # 获取测量结果
# # counts = result.get_counts(circuit)
# # print("测量结果:", counts)
# #
# # # 画出量子电路
# # circuit.draw('mpl')
# # plt.show()
#
# # 简化的RSA加密示例
# def basic_rsa_example():
#     # 两个质数
#     p = 61
#     q = 53
#     n = p * q  # 公钥的一部分
#
#     # 在实际RSA中，这些数字要大得多
#     # 典型的RSA可能使用2048位或更大的数字
#     print(f"n = {n}")  # n = 3233
#
#
# # 传统方法尝试分解n
# def classical_factoring(n):
#     # 非常耗时的过程
#     for i in range(2, int(n ** 0.5) + 1):
#         if n % i == 0:
#             return i, n // i
#     return None
#
#
# import numpy as np
#
#
# def quantum_period_finding(N):
#     """
#     使用量子周期查找来分解数字N
#     这是Shor算法的核心部分
#     """
#     # 计算所需的量子比特数
#     n = len(bin(N)[2:])
#
#     # 创建量子寄存器
#     qr = QuantumRegister(2 * n)
#     cr = ClassicalRegister(n)
#     qc = QuantumCircuit(qr, cr)
#
#     # 初始化第一个寄存器为叠加态
#     for i in range(n):
#         qc.h(i)
#
#     # 添加模幂运算（这是简化版本）
#     # 实际的Shor算法这部分更复杂
#     for i in range(n):
#         qc.cx(i, i + n)
#
#     # 应用逆量子傅立叶变换
#     for i in range(n):
#         for j in range(i):
#             qc.cp(-np.pi / float(2 ** (i - j)), j, i)
#         qc.h(i)
#
#     # 测量
#     qc.measure(range(n), range(n))
#
#     # 执行电路
#     backend = Aer.get_backend('qasm_simulator')
#     job = execute(qc, backend, shots=1000)
#     result = job.result()
#     counts = result.get_counts(qc)
#
#     return counts
#
#
# def improved_shor_demo(N):
#     """
#     改进的Shor算法演示
#     """
#     # 使用Qiskit的Shor算法实现
#     backend = Aer.get_backend('qasm_simulator')
#     quantum_instance = QuantumInstance(backend, shots=1000)
#
#     shor = Shor(quantum_instance=quantum_instance)
#     result = shor.factor(N)
#
#     return result
#
#
# def quantum_vs_classical_comparison():
#     # 测试数字
#     N = 15  # 使用一个小一点的数字作为示例
#
#     print("传统计算方式:")
#     start = time.time()
#     classical_result = classical_factoring(N)
#     classical_time = time.time() - start
#     print(f"结果: {classical_result}")
#     print(f"用时: {classical_time} 秒")
#
#     print("\n量子计算方式:")
#     start = time.time()
#     try:
#         quantum_result = improved_shor_demo(N)
#         quantum_time = time.time() - start
#         print(f"因数: {quantum_result}")
#     except Exception as e:
#         print(f"量子计算出错: {str(e)}")
#     print(f"用时: {quantum_time} 秒")
#
#     print("\n量子周期查找结果:")
#     period_results = quantum_period_finding(N)
#     print(f"周期分布: {period_results}")
#
#
# if __name__ == '__main__':
#
#     quantum_vs_classical_comparison()

def 找出右括号对应的左括号(str_formula):
    stack = []
    for i in range(len(str_formula) - 1, -1, -1):
        if str_formula[i] == ')':
            stack.append(i)
        elif str_formula[i] == '(':
            stack.pop()
            if not stack:
                return i  # 找到了左括号对应的序号
    return -1  # 没找到对应的左括号，说明右括号的个数比左括号的个数多


def 判断最左端和最右端的括号是否是一对(str_formula):
    if str_formula[0] != '(' or str_formula[-1] != ')':
        return False
    left_count = 0
    for i, item in enumerate(str_formula):
        if item == '(':
            left_count += 1
        elif item == ')':
            left_count -= 1
            if left_count == 0:
                if i == len(str_formula) - 1:
                    return True  # 最左端和最右端的括号是一对
                else:
                    return False  # 最左端和最右端的括号不是一对
    return False  # 最左端和最右端的括号不是一对


def 找出分子(str_formula, res=[]):
    原始分子_倒置 = ''
    try:
        left, right = str_formula.split('/', 1)
    except ValueError:
        res.append((str_formula, '', ''))
        return res
    i = len(left) - 1
    while i >= 0:
        # print(原始分子_倒置)
        if left[i] not in ['+', '-', ')']:
            原始分子_倒置 += left[i]
            i -= 1
        elif left[i] == ')':
            左括号的索引 = 找出右括号对应的左括号(left[0:i + 1])
            if 左括号的索引 != -1:
                最接近除号的左右括号之间的子串包括左右括号 = left[左括号的索引:i + 1][::-1]
                原始分子_倒置 += 最接近除号的左右括号之间的子串包括左右括号
                if 左括号的索引 == 0:
                    break
                else:
                    if left[左括号的索引 - 1] == '*':
                        i = 左括号的索引 - 1
                    else:
                        break
            else:
                原始分子_倒置 += left[i]
                i -= 1
        elif left[i] in ['+', '-']:
            break
    # 去掉最左边和最右边的括号
    原始分子 = 原始分子_倒置[::-1]
    if 判断最左端和最右端的括号是否是一对(原始分子):
        分子 = 原始分子[1:-1]  # 去掉最左边和最右边的括号
    else:
        分子 = 原始分子
    res.append((left, 分子, right))
    找出分子(right, res)
    return res


if __name__ == '__main__':
    res = 找出分子('( a / b + c ) / (d + e / f ) + g')
    for item in res:
        print(item)
