def validate_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                raise ValueError("Value must be non-negative.")
            return value
        except ValueError as e:
            print(f"Invalid input. {e}")

def compute_spam_given_free():
    print("Enter the following details:")
    total_emails = validate_positive_int("Total emails: ")
    emails_with_free = validate_positive_int("Emails containing 'free': ")
    spam_emails = validate_positive_int("Spam emails: ")
    spam_and_free = validate_positive_int("Emails that are both spam and contain 'free': ")

    if total_emails == 0 or spam_emails == 0 or emails_with_free == 0:
        print("Error: Counts must be greater than 0 to compute probabilities.")
        return

    if spam_emails > total_emails or emails_with_free > total_emails or spam_and_free > spam_emails:
        print("Error: Invalid input relationships.")
        return

    # Bayes' Theorem
    p_spam = spam_emails / total_emails
    p_free = emails_with_free / total_emails
    p_free_given_spam = spam_and_free / spam_emails

    p_spam_given_free = (p_free_given_spam * p_spam) / p_free

    print(f"\nP(Spam | Free): {p_spam_given_free:.4f}")

# Run it
compute_spam_given_free()
