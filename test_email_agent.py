from agents.email_agent import process_email

if __name__ == "__main__":
    file_path = "sample_inputs/complaint_email.txt"
    result = process_email(file_path)
    print("\n📨 Email Agent Output:")
    for k, v in result.items():
        print(f"{k}: {v}")
