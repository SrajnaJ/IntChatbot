from app.services.qa_service import QAService

def main():
    qa = QAService()
    question = "how many family day leaves do i have?"
    answer = qa.answer(question)

    print("\nANSWER:\n")
    print(answer)


if __name__ == "__main__":
    main()
