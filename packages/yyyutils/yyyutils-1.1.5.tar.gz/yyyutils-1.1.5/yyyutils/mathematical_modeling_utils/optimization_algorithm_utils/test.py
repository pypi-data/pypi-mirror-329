class OptimizationAlgorithmUtils:
    def simulated_annealing(self, func, x0, T_max=1000, T_min=1e-8, L=100, max_stay_counter=100, verbose=False):
        """
        退火算法
        :param func: 目标函数
        :param x0: 初始解
        :param T_max: 初始温度
        :param T_min: 最低温度
        :param L: 冷却长度
        :param max_stay_counter: 最大停留计数器
        :param verbose: 是否打印详细信息
        """
        from sko.SA import SA
        sa = SA(func=func, n_dim=1, x0=x0, T_max=T_max, T_min=T_min, L=L, max_stay_counter=max_stay_counter,
                verbose=verbose)
        best_x, best_y = sa.run()
        return best_x, best_y

    def particle_swarm_optimization(self, func, x0, swarm_size=100, c1=2, c2=2, w=0.8, max_iter=100, verbose=False):
        """
        粒子群算法
        :param func: 目标函数
        :param x0: 初始解
        :param swarm_size: 粒子群大小
        :param c1: 个体学习因子
        :param c2: 社会学习因子
        :param w: 惯性权重
        :param max_iter: 最大迭代次数
        :param verbose: 是否打印详细信息
        """
        from sko.PSO import PSO
        pso = PSO(func=func, n_dim=1, pop=swarm_size, c1=c1, c2=c2, w=w, max_iter=max_iter, verbose=verbose)
        best_x, best_y = pso.run()
        return best_x, best_y

    def genetic_algorithm(self, func, x0, pop_size=100, pc=0.8, pm=0.01, max_iter=100, verbose=False):
        """
        遗传算法
        :param func: 目标函数
        :param x0: 初始解
        :param pop_size: 种群大小
        :param pc: 交叉概率
        :param pm: 变异概率
        :param max_iter: 最大迭代次数
        :param verbose: 是否打印详细信息
        """
        from sko.GA import GA
        ga = GA(func=func, n_dim=1, size_pop=pop_size, max_iter=max_iter, prob_mut=pm, prob_cross=pc, verbose=verbose)
        best_x, best_y = ga.run()
        return best_x, best_y

    def ant_colony_optimization(self, func, x0, n_dim, max_iter=100, alpha=1, beta=1, rho=0.5, Q=100, verbose=False):
        """
        蚁群优化算法
        :param func: 目标函数
        :param x0: 初始解
        :param n_dim: 问题的维度
        :param max_iter: 最大迭代次数
        :param alpha: 信息素重要度的参数
        :param beta: 启发式因子的重要度
        :param rho: 信息素的蒸发率
        :param Q: 信息素强度
        :param verbose: 是否打印详细信息
        """
        from sko.ACA import ACA
        aco = ACA(func=func, n_dim=n_dim, size_pop=50, max_iter=max_iter, alpha=alpha, beta=beta, rho=rho, Q=Q,
                  verbose=verbose)
        best_x, best_y = aco.run()
        return best_x, best_y

    def firefly_algorithm(self, func, x0, n_dim, max_iter=100, alpha=0.2, beta0=1, gamma=1, verbose=False):
        """
        火焰优化算法
        :param func: 目标函数
        :param x0: 初始解
        :param n_dim: 问题的维度
        :param max_iter: 最大迭代次数
        :param alpha: 吸引程度的参数
        :param beta0: 吸引程度的初始值
        :param gamma: 光强的衰减系数
        :param verbose: 是否打印详细信息
        """
        from sko.FA import FA
        fa = FA(func=func, n_dim=n_dim, size_pop=50, max_iter=max_iter, alpha=alpha, beta0=beta0, gamma=gamma,
                verbose=verbose)
        best_x, best_y = fa.run()
        return best_x, best_y

    def entropy_optimization(self, func, x0, n_dim, max_iter=100, eta=1e-4, verbose=False):
        """
        熵优化算法
        :param func: 目标函数
        :param x0: 初始解
        :param n_dim: 问题的维度
        :param max_iter: 最大迭代次数
        :param eta: 学习率
        :param verbose: 是否打印详细信息
        """
        from sko.EO import EO
        eo = EO(func=func, n_dim=n_dim, size_pop=50, max_iter=max_iter, eta=eta, verbose=verbose)
        best_x, best_y = eo.run()
        return best_x, best_y

    def gradient_based_optimization(self, func, x0, n_dim, max_iter=100, learning_rate=0.01, verbose=False):
        """
        基于梯度的优化算法
        :param func: 目标函数
        :param x0: 初始解
        :param n_dim: 问题的维度
        :param max_iter: 最大迭代次数
        :param learning_rate: 学习率
        :param verbose: 是否打印详细信息
        """
        from sko.GBO import GBO
        gbo = GBO(func=func, n_dim=n_dim, size_pop=50, max_iter=max_iter, learning_rate=learning_rate, verbose=verbose)
        best_x, best_y = gbo.run()
        return best_x, best_y
