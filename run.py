from yal_agent.classifier import classify

message = input("Guest message: ")

result = classify(message)

print("\nResult:")
print(result)