import time

DOMAIN = (1, 2, 3, 4, 5)
DIM = len(DOMAIN)


def clone_grid(rel_grid):
    return [row[:] for row in rel_grid]


def render_grid(rel_grid, label=""):
    if label:
        print(f"[{label}]")
    for row in rel_grid:
        print(" ".join(str(bit) for bit in row))


def input_relation_grid():
    print("관계행렬을 입력하세요:")
    return [list(map(int, input(f"{row_idx + 1}행: ").split())) for row_idx in range(DIM)]


def verify_reflexive(rel_grid):
    return all(rel_grid[idx][idx] == 1 for idx in range(DIM))


def verify_symmetric(rel_grid):
    for r in range(DIM):
        for c in range(r + 1, DIM):
            if rel_grid[r][c] != rel_grid[c][r]:
                return False
    return True


def verify_transitive(rel_grid):
    for src in range(DIM):
        for mid in range(DIM):
            if rel_grid[src][mid] == 1:
                for dst in range(DIM):
                    if rel_grid[mid][dst] == 1 and rel_grid[src][dst] == 0:
                        return False
    return True


def judge_equivalence(rel_grid):
    ref_ok = verify_reflexive(rel_grid)
    sym_ok = verify_symmetric(rel_grid)
    tra_ok = verify_transitive(rel_grid)

    print("\n--- 관계 성질 판별 결과 ---")
    print(f"반사 관계: {'성립' if ref_ok else '불성립'}")
    print(f"대칭 관계: {'성립' if sym_ok else '불성립'}")
    print(f"추이 관계: {'성립' if tra_ok else '불성립'}")

    if ref_ok and sym_ok and tra_ok:
        print("=> 이 관계는 동치 관계입니다.")
    else:
        print("=> 이 관계는 동치 관계가 아닙니다.")

    return ref_ok, sym_ok, tra_ok


def extract_equiv_class(rel_grid, target):
    row_idx = target - 1
    return [DOMAIN[col_idx] for col_idx in range(DIM) if rel_grid[row_idx][col_idx] == 1]


def display_equiv_classes(rel_grid):
    print("\n--- 각 원소의 동치류 ---")
    for elem in DOMAIN:
        members = extract_equiv_class(rel_grid, elem)
        formatted = ", ".join(map(str, members))
        print(f"[{elem}] = {{{formatted}}}")


def build_reflexive_closure(rel_grid):
    closed = clone_grid(rel_grid)
    for idx in range(DIM):
        closed[idx][idx] = 1
    return closed


def build_symmetric_closure(rel_grid):
    closed = clone_grid(rel_grid)
    for r in range(DIM):
        for c in range(DIM):
            if closed[r][c] == 1:
                closed[c][r] = 1
    return closed


def build_transitive_closure(rel_grid):
    closed = clone_grid(rel_grid)
    for pivot in range(DIM):
        for src in range(DIM):
            if closed[src][pivot] == 1:
                for dst in range(DIM):
                    if closed[pivot][dst] == 1:
                        closed[src][dst] = 1
    return closed


def execute():
    origin_grid = input_relation_grid()
    start_ts = time.perf_counter()

    ref_ok, sym_ok, tra_ok = judge_equivalence(origin_grid)

    if ref_ok and sym_ok and tra_ok:
        display_equiv_classes(origin_grid)
    else:
        working_grid = clone_grid(origin_grid)
        closure_pipeline = [
            ("반사 폐포", verify_reflexive, build_reflexive_closure),
            ("대칭 폐포", verify_symmetric, build_symmetric_closure),
            ("추이 폐포", verify_transitive, build_transitive_closure),
        ]

        for title, checker, builder in closure_pipeline:
            if not checker(working_grid):
                print(f"\n========== {title} 적용 ==========")
                before_grid = clone_grid(working_grid)
                working_grid = builder(working_grid)

                render_grid(before_grid, f"{title} 변환 전")
                render_grid(working_grid, f"{title} 변환 후")

        r_ok, s_ok, t_ok = judge_equivalence(working_grid)
        if r_ok and s_ok and t_ok:
            display_equiv_classes(working_grid)

    elapsed_ms = (time.perf_counter() - start_ts) * 1000
    print(f"\n[총 연산 소요 시간: {elapsed_ms:.4f} ms]")


if __name__ == "__main__":
    execute()
