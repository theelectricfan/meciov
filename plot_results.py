import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_all(csv_path="results/auction_log.csv", out_dir="results/plots"):
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    os.makedirs(out_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    # Clean NaNs if any
    df = df.dropna(subset=["vehicle_id", "assigned"])

    # ✅ Success Rate
    success_rate = df["assigned"].sum() / len(df)
    print(f"✅ Success Rate: {success_rate*100:.2f}%")

    # ✅ Revenue per SBS
    revenue_df = df[df["assigned"] == True]
    revenue_per_sbs = revenue_df.groupby("sbs_id")["bid_price"].sum().sort_values()

    plt.figure(figsize=(10,6))
    revenue_per_sbs.plot(kind="bar", color="skyblue")
    plt.title("📈 Revenue per SBS")
    plt.xlabel("SBS ID")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/revenue_per_sbs.png")
    plt.close()

    # ✅ Delay Histogram
    plt.figure(figsize=(8,5))
    sns.histplot(df["total_delay_ms"], bins=30, kde=True, color="orange")
    plt.title("⏱ Task Total Delay Distribution")
    plt.xlabel("Total Delay (ms)")
    plt.ylabel("Task Count")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/delay_histogram.png")
    plt.close()

    # ✅ Satisfaction Histogram
    plt.figure(figsize=(8,5))
    sns.histplot(df["satisfaction_score"], bins=20, kde=True, color="purple")
    plt.title("📉 Histogram of Satisfaction Scores")
    plt.xlabel("Satisfaction Score")
    plt.ylabel("Vehicle Count")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/satisfaction_histogram.png")
    plt.close()

    # ✅ Satisfaction CDF
    plt.figure(figsize=(8,5))
    sorted_scores = df["satisfaction_score"].sort_values()
    cdf = sorted_scores.rank(method="average", pct=True)
    plt.plot(sorted_scores, cdf, marker=".")
    plt.title("📊 CDF of Satisfaction Scores")
    plt.xlabel("Satisfaction Score")
    plt.ylabel("CDF")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/satisfaction_cdf.png")
    plt.close()

    # ✅ Deadline Violation Pie Chart
    df["deadline_violation"] = df["total_delay_ms"] > df["task_deadline_ms"]
    violations = df["deadline_violation"].sum()
    non_violations = (~df["deadline_violation"]).sum()

    plt.figure(figsize=(6,6))
    plt.pie([violations, non_violations], labels=["Violated", "Met"], autopct="%1.1f%%", colors=["#FF9999", "#99FF99"])
    plt.title("⚠️ Deadline Violations")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/deadline_violations.png")
    plt.close()

    print(f"📁 Plots saved to: {out_dir}")

# ✅ Entry point
if __name__ == "__main__":
    plot_all()
