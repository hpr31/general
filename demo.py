def solve():
    try:
        n = int(input().strip())
    except:
        return
    
    recipes = {}
    
    for _ in range(n):
        s = input().strip()
        if not s:
            continue
        left, right = s.split("=")
        ingredients = right.split("+")
        recipes.setdefault(left, []).append(ingredients)
    
    target = input().strip()
    memo = {}
    
    def min_orbs(p):
        if p not in recipes:  # base item
            return 0
        if p in memo:
            return memo[p]
        
        best = float("inf")
        for ing_list in recipes[p]:
            cost = len(ing_list) - 1
            for ing in ing_list:
                cost += min_orbs(ing)
            best = min(best, cost)
        
        memo[p] = best
        return best
    
    print(min_orbs(target))

# run solve when executed directly
if __name__ == "__main__":
    solve()
