import matplotlib as plt

def get_items_to_prompt(shared_names: list[str]) -> str:

    for index, name in enumerate(shared_names):
        print(f"{index + 1}: {name}")
    
    while True:
        ans = input("Enter the index of the item you would like to graph: ")

        try:
            ans = int(ans)
            ans_name = shared_names[ans]
        except (ValueError, IndexError):
            print(f"{ans} is not a valid index.")
            continue
        break
    return ans_name
        




    

    