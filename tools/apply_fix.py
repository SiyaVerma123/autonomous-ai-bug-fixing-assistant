import os


def apply_fix(repo_path, file_path, fixed_code):
    """
    Apply a validated fix to the original repository.
    """

    target_file = os.path.join(
        repo_path,
        file_path
    )

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    return target_file