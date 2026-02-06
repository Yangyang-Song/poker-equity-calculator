import numpy as np

def estimate_pi_optimized(n):
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)
    
    points_inside = np.sum(x**2 + y**2 <= 1)
    
    pi_estimate = 4 * points_inside / n
    
    return pi_estimate, points_inside

def main():
    try:
        n = int(input("Please input the number of experiments n: "))
        if n <= 0:
            print("Please enter an integer greater than 0!")
            return
    except ValueError:
        print("Please enter a valid integer!")
        return
    
    pi_estimate, points_inside = estimate_pi_optimized(n)
    
    print(f"\nMonte Carlo π Estimation Results")
    print(f"Number of Experiments: {n:,}")
    print(f"Points Inside Circle: {points_inside:,}")
    print(f"Estimated π ≈ {pi_estimate:.10f}")
    print(f"Absolute Error from True π: {abs(pi_estimate - np.pi):.8e}")
    print(f"Relative Error: {abs(pi_estimate - np.pi)/np.pi * 100:.6f}%")
    
    if n > 100:
        p_estimate = points_inside / n
        theoretical_std = 4 * np.sqrt(p_estimate * (1 - p_estimate) / n)
        
        print(f"\nerror analysis (n > 100)")
        print(f"Theoretical Standard Deviation: ±{theoretical_std:.6e}")
        print(f"95% Confidence Interval: [{pi_estimate - 1.96*theoretical_std:.8f}, {pi_estimate + 1.96*theoretical_std:.8f}]")
    
        actual_error = abs(pi_estimate - np.pi)
        efficiency = theoretical_std / actual_error if actual_error > 0 else float('inf')
        print(f"Actual Error / Theoretical Error Ratio: {efficiency:.3f}")

if __name__ == "__main__":
    main()
