import math


class SoilPressure:
    def __init__(self, debug=True):
        self.debug = debug

    def _calculate_trapezoidal_centroid_to_low(self, a=0, b=0, h=0):
        """
        计算梯形截面质心到低端的距离
        :return:
        """
        if a > b:
            a, b = b, a
        return (3 * a * h + h * b - h * a) / 3 / (a + b)

    def calculate_resting_soil_pressure(self, q=0, K0=0, gamma=0, H=0):
        """
        计算静止土压力
        """
        res = (q + 0.5 * gamma * H) * H * K0
        if self.debug:
            print("\n静止土压力计算:")
            print("理论公式: σ0 = (q + 0.5γH)HK0")
            print(f"代入计算: σ0 = ({q} + 0.5 × {gamma} × {H}) × {H} × {K0} = {round(res, 2)}")
        return res

    def calculate_sandy_soil_K0(self, fai_):
        """
        计算砂性土的静止土压力系数K0
        """
        res = 1 - math.sin(math.radians(fai_))
        if self.debug:
            print("\n砂性土的静止土压力系数计算:")
            print("理论公式: K0 = 1 - sinφ")
            print(f"代入计算: K0 = 1 - sin{fai_}° = {round(res, 2)}")
        return res

    def calculate_sticky_soil_K0(self, fai_):
        """
        计算粘性土的静止土压力系数K0
        """
        res = 0.95 - math.sin(math.radians(fai_))
        if self.debug:
            print("\n粘性土的静止土压力系数计算:")
            print("理论公式: K0 = 0.95 - sinφ")
            print(f"代入计算: K0 = 0.95 - sin{fai_}° = {round(res, 2)}")
        return res

    def calculate_super_consolidated_sticky_soil_K0(self, fai_, OCR):
        """
        计算超固结粘性土的静止土压力系数K0
        """
        res = OCR ** 0.5 * (1 - math.sin(math.radians(fai_)))
        if self.debug:
            print("\n超固结粘性土的静止土压力系数计算:")
            print("理论公式: K0 = OCR^0.5 × (1 - sinφ)")
            print(f"代入计算: K0 = {OCR}^0.5 × (1 - sin{fai_}°) = {round(res, 2)}")
        return res

    def _calculate_active_soil_pressure(self, q=0, Ka=0, gamma=0, H=0, c=0):
        """
        计算主动土压力
        """
        res = (q + gamma * H) * Ka - 2 * c * Ka ** 0.5
        if self.debug:
            print(f"\n深度H={H}处的主动土压力计算:")
            print("理论公式: Pa = (q + γH)Ka - 2c√Ka")
            print(f"代入计算: Pa = ({q} + {gamma} × {H}) × {Ka} - 2 × {c} × {round(Ka ** 0.5, 4)} = {round(res, 2)}")
        return res

    def calculate_Ka(self, fai):
        """
        计算主动土压力系数Ka
        """
        res = math.tan(math.radians(45 - fai / 2)) ** 2
        if self.debug:
            print("\n主动土压力系数计算:")
            print("理论公式: Ka = tan²(45° - φ/2)")
            print(f"代入计算: Ka = tan²(45° - {fai}°/2) = {round(res, 2)}")
        return res

    def calculate_Kp(self, fai):
        """
        计算被动土压力系数Kp
        """
        res = math.tan(math.radians(45 + fai / 2)) ** 2
        if self.debug:
            print("\n被动土压力系数计算:")
            print("理论公式: Kp = tan²(45° + φ/2)")
            print(f"代入计算: Kp = tan²(45° + {fai}°/2) = {round(res, 2)}")
        return res

    def _calculate_z0(self, q=0, Ka=0, gamma=0, c=0):
        """
        计算主动土应力正负分界点的深度z0
        """
        res = (2 * c / Ka ** 0.5 - q) / gamma
        if self.debug:
            print("\n主动土应力正负分界点深度计算:")
            print("理论公式: z0 = (2c/√Ka - q)/γ")
            print(f"代入计算: z0 = (2 × {c}/√{Ka} - {q})/{gamma} = {round(res, 2)}")
        return res

    def calculate_active_soil_pressure(self, q=0, Ka=0, gamma=0, H=0, c=0):
        """
        计算主动土压力
        """
        if self.debug:
            print("\n计算主动土压力:")
        z0 = self._calculate_z0(q, Ka, gamma, c)
        min_active_stress = self._calculate_active_soil_pressure(q, Ka, gamma, 0, c)
        max_active_stress = self._calculate_active_soil_pressure(q, Ka, gamma, H, c)
        Ea = 0.5 * max_active_stress * (H - z0)
        h = (H - z0) / 3 if z0 > 0 else self._calculate_trapezoidal_centroid_to_low(min_active_stress,
                                                                                    max_active_stress, H)
        if self.debug:
            print("\n主动土压合力计算:")
            print("理论公式: Ea = 0.5 × Pa × (H - z0)")
            print(f"代入计算: Ea = 0.5 × {round(max_active_stress, 2)} × ({H} - {round(z0, 2)}) = {round(Ea, 2)}")
            print("\n作用点距墙底距离:", h)
        return Ea, h

    def _calculate_passive_soil_pressure(self, q=0, Kp=0, gamma=0, H=0, c=0):
        """
        计算某一深度处的被动土压力
        """
        res = (q + gamma * H) * Kp + 2 * c * Kp ** 0.5
        if self.debug:
            print(f"\n深度H={H}处的被动土压力计算:")
            print("理论公式: Pp = (q + γH)Kp + 2c√Kp")
            print(f"代入计算: Pp = ({q} + {gamma} × {H}) × {Kp} + 2 × {c} × {round(Kp ** 0.5, 4)} = {round(res, 2)}")
        return res

    def calculate_passive_soil_pressure(self, q=0, Kp=0, gamma=0, H=0, c=0):
        """
        计算被动土压力
        """
        if self.debug:
            print("\n计算被动土压力:")
        max_passive_stress = self._calculate_passive_soil_pressure(q, Kp, gamma, H, c)
        min_passive_stress = self._calculate_passive_soil_pressure(q, Kp, gamma, 0, c)
        Ep = 0.5 * (max_passive_stress + min_passive_stress) * H
        h = self._calculate_trapezoidal_centroid_to_low(min_passive_stress, max_passive_stress, H)

        if self.debug:
            print("\n被动土压合力计算:")
            print("理论公式: Ep = 0.5 × (Ppmax + Ppmin) × H")
            print(
                f"代入计算: Ep = 0.5 × ({round(max_passive_stress, 2)} + {round(min_passive_stress, 2)}) × {H} = {round(Ep, 2)}")
            print("\n作用点距墙底距离:", h)
        return Ep, h

    def _calculate_resting_water_pressure(self, gammaw=0, H=0, hw=0):
        """
        计算某一深度处的静水压力
        :param gammaw:水的重度
        :param H: 某一深度
        :param hw: 水的水位深度
        :return:
        """
        res = gammaw * (H - hw) if H > hw else 0
        if self.debug:
            print(f"\n深度H={H}处的静水压力计算:")
            print("理论公式: Pw = γw(H - hw)")
            print(f"代入计算: Pw = {gammaw} × ({H} - {hw}) = {round(res, 2)}")
        return res

    def calculate_resting_water_pressure(self, gammaw=0, H1=0, H2=0, hw=0):
        """
        计算静水总压力
        :param gammaw:水的重度
        :param H: 某一深度
        :param hw: 水的水位深度
        :return:
        """
        if self.debug:
            print("\n计算静水总压力:")
        if H1 > H2:
            H1, H2 = H2, H1
        if H1 <= hw:
            H1 = hw
        if H2 <= hw:
            print("静水总压力：0")
            return 0
        res = 0.5 * (self._calculate_resting_water_pressure(gammaw, H1, hw) + self._calculate_resting_water_pressure(
            gammaw, H2, hw) * (H2 - H1))
        if self.debug:
            print(f"\n深度H1={H1}到H2={H2}处的静水总压力计算:")
            print("理论公式: Pw = 0.5 × (Pw1 + Pw2(H2 - H1))")
            print(f"代入计算: Pw = 0.5 × ({self._calculate_resting_water_pressure(gammaw, H1, hw)} + "
                  f"{self._calculate_resting_water_pressure(gammaw, H2, hw)} × ({H2} - {H1})) = {round(res, 2)}")
        return res


if __name__ == '__main__':
    # debug=True时显示计算过程，debug=False时只返回结果
    su = SoilPressure(debug=True)
    Ka = su.calculate_Ka(18)
    Kp = su.calculate_Kp(18)
    z0 = su._calculate_z0(10, Ka, 17.5, 16.2)
    su._calculate_active_soil_pressure(10, Ka, 17.5, 8.5, 16.2)
    su.calculate_active_soil_pressure(10, Ka, 17.5, 8.5, 16.2)
