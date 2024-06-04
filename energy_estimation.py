def main() -> None:
    # CPU: 13th Gen Intel© Core™ i7-1365U × 10 (10 cores, 12 threads)
    # main reference for calculations (including units): https://doi.org/10.1002/advs.202100707 (Green Algorithms paper)
    # using 2023 values for updated carbon intensity (instead of 2020 values used in Green Algorithms paper)

    import time

    # running/processing time (hours, divided from milliseconds)
    t: float = int(input("Enter processing time (in milliseconds): " )) / 3_600_000.0

    # number of cpu cores
    nc: float = 10.0 # source: https://ark.intel.com/content/www/us/en/ark/products/232141/intel-core-i7-1365u-processor-12m-cache-up-to-5-20-ghz.html (Total cores)

    # power draw/consumption of a computing core (W), aka thermal design power (TDP)
    Pc: float = 15.0 # source: https://ark.intel.com/content/www/us/en/ark/products/232141/intel-core-i7-1365u-processor-12m-cache-up-to-5-20-ghz.html (Processor base power)

    # core usage factor (between 0 and 1)
    uc: float = int(input("How much did the CPU use (write as an integer percentage): ")) / 100.0

    # memory (GB)
    nm: int = int(input("How much RAM did the process use, rounded up/down (in GB): ")) 

    # power draw/consumption of memory (W)
    Pm: float = nm * 0.3725 # source: https://doi.org/10.1002/advs.202100707 (Green Algorithms paper, Section 5)

    # power usage effectiveness - used to factor in repeated computations of an algorithm
    PUE: float = 1.0 # assume average (sources: https://www.42u.com/measurement/pue-dcie.htm, https://www.42u.com/wp-content/uploads/pueEfficiencyDiagram.png)

    # energy consumption estimate (mWh)
    E: float = t * (nc * Pc * uc + nm * Pm) * PUE * 1000 # 1000 = conversion from W to mW
    print(f"Estimated energy consumption: {E} (mWh)")

    # # carbon intensity of energy production (gCO2e/kWh, multiplied from kgCO2e/kWh)
    # CI: float = 0.2249894 * 1000.0 # source: https://www.carbonfootprint.com/docs/2023_07_international_factors_release_11.xlsx (see GB/United Kingdom, Total Production fuel mix factor)

    # # carbon footprint estimate (gCO2e)
    # C: float = (E / 0.000001) * CI # 0.000001 = conversion from mWh to kWh
    # print(f"Estimated carbon footprint: {C} (gCO2e)")

if __name__=="__main__":
    main()
