# legacy_graffiti.py
import time
from functools import partial
from itertools import combinations, product
from tqdm import tqdm
import numpy as np
import pandas as pd
import logging

# Import candidate operations.
from graffitiai.experimental.candidate_operations import (
    identity_func, square_func, floor_func, ceil_func,
    add_ratio_func, sub_ratio_func, multiply_ratio_func,
    add_columns_func, subtract_columns_func, subtract_columns_func_reversed,
    multiply_columns_func, max_columns_func, min_columns_func,
    abs_diff_columns_func, safe_division_func, safe_division_func_reversed,
    mod_func, sqrt_func
)

# Import candidate transformations.
from graffitiai.experimental.candidate_transformations import (
    floor_transform, ceil_transform,
    add_ratio_transform, sub_ratio_transform, multiply_ratio_transform,
    sqrt_transform
)

__all__ = [
    "LegacyGraffiti"
]

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class LegacyGraffiti:
    def __init__(self, df, target_invariant, bound_type='lower', filter_property=None, time_limit=None):
        self.df_full = df.copy()
        if filter_property is not None:
            self.df = df[df[filter_property] == True].copy()
            self.hypothesis_str = filter_property
        else:
            self.df = df.copy()
            self.hypothesis_str = None

        self.target = target_invariant
        self.bound_type = bound_type  # 'lower' or 'upper'
        self.time_limit = time_limit  # in seconds

        # Candidate columns: numeric (but not boolean) and not the target.
        self.candidate_cols = [
            col for col in self.df.columns
            if col != target_invariant and
               pd.api.types.is_numeric_dtype(self.df[col]) and
               not pd.api.types.is_bool_dtype(self.df[col])
        ]

        self.accepted_conjectures = []
        self.max_complexity = 7

        # A list of Fraction constants used in ratio operations.
        from fractions import Fraction
        self.ratios = [
            Fraction(1, 10), Fraction(3, 10), Fraction(7, 10), Fraction(9, 10),
            Fraction(1, 9), Fraction(2, 9), Fraction(4, 9), Fraction(5, 9),
            Fraction(7, 9), Fraction(8, 9), Fraction(10, 9),
            Fraction(1, 8), Fraction(3, 8), Fraction(5, 8), Fraction(7, 8), Fraction(9, 8),
            Fraction(1, 7), Fraction(2, 7), Fraction(3, 7), Fraction(4, 7), Fraction(5, 7),
            Fraction(6, 7), Fraction(8, 7), Fraction(9, 7),
            Fraction(1, 6), Fraction(5, 6), Fraction(7, 6),
            Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(6, 5),
            Fraction(7, 5), Fraction(8, 5), Fraction(9, 5),
            Fraction(1, 4),
            Fraction(1, 3), Fraction(2, 3), Fraction(4, 3), Fraction(5, 3),
            Fraction(7, 3), Fraction(8, 3), Fraction(10, 3),
            Fraction(1, 2), Fraction(3, 2), Fraction(5, 2), Fraction(7, 2), Fraction(9, 2),
            Fraction(1, 1), Fraction(2, 1),
             # Fraction(3, 1), Fraction(4, 1),
        ]

    # -------------------- Candidate Generation --------------------
    def _generate_candidates_unary(self, col):
        # Use list comprehensions to generate all unary candidates quickly.
        base = [
            (f"{col}", partial(identity_func, col=col)),
            (f"({col})^2", partial(square_func, col=col)),
            (f"floor({col})", partial(floor_func, col=col)),
            (f"ceil({col})", partial(ceil_func, col=col))
        ]
        # Include ratio multiplication, addition, and subtraction.
        mult_candidates = [(f"{col} * {ratio}", partial(multiply_ratio_func, col=col, ratio=ratio))
                           for ratio in self.ratios]
        add_candidates = [(f"({col}) + {ratio}", partial(add_ratio_func, col=col, ratio=ratio))
                          for ratio in self.ratios]
        sub_candidates = [(f"({col}) - {ratio}", partial(sub_ratio_func, col=col, ratio=ratio))
                          for ratio in self.ratios]
        return base + mult_candidates + add_candidates + sub_candidates

    def _generate_candidates_binary(self, col1, col2):
        # Use a list comprehension where possible.
        candidates = [
            (f"({col1} + {col2})", partial(add_columns_func, col1=col1, col2=col2)),
            (f"({col1} - {col2})", partial(subtract_columns_func, col1=col1, col2=col2)),
            (f"({col2} - {col1})", partial(subtract_columns_func_reversed, col1=col1, col2=col2)),
            (f"{col1} * {col2}", partial(multiply_columns_func, col1=col1, col2=col2)),
            (f"max({col1}, {col2})", partial(max_columns_func, col1=col1, col2=col2)),
            (f"min({col1}, {col2})", partial(min_columns_func, col1=col1, col2=col2)),
            (f"abs({col1} - {col2})", partial(abs_diff_columns_func, col1=col1, col2=col2)),
            (f"{col1}*{col2}", partial(multiply_columns_func, col1=col1, col2=col2))
        ]
        if (self.df[col2] == 0).sum() == 0:
            candidates.append((f"({col1} / {col2})", partial(safe_division_func, col1=col1, col2=col2)))
        if (self.df[col1] == 0).sum() == 0:
            candidates.append((f"({col2} / {col1})", partial(safe_division_func_reversed, col1=col1, col2=col2)))
        # Add modulus candidate.
        candidates.append((f"({col1} mod {col2})", partial(mod_func, col1=col1, col2=col2)))

        return candidates

    # def _generate_candidates_trinary(self, col1, col2, col3):
    #     # Use a list comprehension where possible.
    #     candidates = [
    #         (f"({col1} + {col2} + {col3})", partial(add_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"({col1} - {col2} - {col3})", partial(subtract_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"({col2} - {col1} - {col3})", partial(subtract_columns_func_reversed, col1=col1, col2=col2, col3=col3)),
    #         (f"{col1} * {col2} * {col3}", partial(multiply_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"max({col1}, {col2}, {col3})", partial(max_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"min({col1}, {col2}, {col3})", partial(min_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"abs({col1} - {col2} - {col3})", partial(abs_diff_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"{col1}*{col2}*{col3}", partial(multiply_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"({col1} + {col2}) * {col3}", partial(multiply_columns_func, col1=col1, col2=col2, col3=col3)),
    #         (f"({col1} - {col2}) * {col3}", partial(multiply_columns_func, col1=col1, col2=col2, col3=col3)),
    #     ]
    #     return candidates

    def _generate_candidates_complex_mod_sqrt(self):
        # Use combinations from itertools.
        candidates = []
        for a, n, d in combinations(self.candidate_cols, 3):
            def candidate_func(df, a=a, n=n, d=d):
                mod_val = mod_func(df, n, d)
                one_plus = 1 + mod_val
                product_val = df[a] * one_plus
                sqrt_val = np.sqrt(product_val)
                return np.ceil(sqrt_val)
            expr_str = f"CEIL(sqrt({a} * (1 + ({n} mod {d}))))"
            candidates.append((expr_str, candidate_func))
        return candidates

    def _generate_candidates_max_of_three(self):
        # Use combinations from itertools.
        candidates = []
        for a, n, d in combinations(self.candidate_cols, 3):
            def candidate_func(df, a=a, n=n, d=d):
                return np.maximum(df[a], np.maximum(df[n], df[d]))
            expr_str = f"max({a}, max({n}, {d}))"
            candidates.append((expr_str, candidate_func))
        return candidates

    def _generate_candidates_min_of_three(self):
        # Use combinations from itertools.
        candidates = []
        for a, n, d in combinations(self.candidate_cols, 3):
            def candidate_func(df, a=a, n=n, d=d):
                return np.minimum(df[a], np.minimum(df[n], df[d]))
            expr_str = f"min({a}, min({n}, {d}))"
            candidates.append((expr_str, candidate_func))
        return candidates

    def _generate_candidates_linear_combination(self, num_terms=2):
        """
        Generate candidates of the form:
          ratio1*inv1 + (or -) ratio2*inv2 + (or -) ratio3*inv3
        using the identity candidate for each invariant.
        """
        candidates = []
        # Build base candidates using each candidate column.
        base_candidates = [(f"{col}", partial(identity_func, col=col)) for col in self.candidate_cols]
        for combo in combinations(base_candidates, num_terms):
            for ratios in product(self.ratios, repeat=num_terms):
                for signs in product([1, -1], repeat=num_terms):
                    # Build the expression string.
                    expr_parts = [f"{'' if s > 0 else '-'}{ratio}*({expr})"
                                  for (expr, _), ratio, s in zip(combo, ratios, signs)]
                    candidate_expr = " + ".join(expr_parts).replace("+ -", "- ")
                    # Define a candidate function that sums the contributions.
                    def candidate_func(df, combo=combo, ratios=ratios, signs=signs):
                        total = 0
                        for (_, func_i), ratio, s in zip(combo, ratios, signs):
                            total += s * float(ratio) * func_i(df)
                        return total
                    candidates.append((candidate_expr, candidate_func))
        return candidates

    # -------------------- Candidate Transformations --------------------
    def _with_floor_ceil(self, candidate):
        base_rhs, base_func = candidate
        return [(f"floor({base_rhs})", partial(floor_transform, base_func=base_func)),
                (f"ceil({base_rhs})", partial(ceil_transform, base_func=base_func))]

    def _with_ratio_addition(self, candidate):
        base_rhs, base_func = candidate
        return [(f"({base_rhs}) + {ratio}", partial(add_ratio_transform, base_func=base_func, ratio=ratio))
                for ratio in self.ratios]

    def _with_ratio_subtraction(self, candidate):
        base_rhs, base_func = candidate
        return [(f"({base_rhs}) - {ratio}", partial(sub_ratio_transform, base_func=base_func, ratio=ratio))
                for ratio in self.ratios]

    def _with_ratio_multiplication(self, candidate):
        base_rhs, base_func = candidate
        return [(f"{ratio}*({base_rhs})", partial(multiply_ratio_transform, base_func=base_func, ratio=ratio))
                for ratio in self.ratios]

    def _expand_candidate(self, candidate):
        variants = {candidate[0]: candidate}
        for transform_func in [self._with_floor_ceil, self._with_ratio_multiplication,
                               self._with_ratio_subtraction, self._with_ratio_addition]:
            for cand in transform_func(candidate):
                variants.setdefault(cand[0], cand)
        return list(variants.values())

    # -------------------- Search Loop --------------------
    def search(self):
        start_time = time.time()
        new_found = True
        logging.info("Starting the search process...")
        # Cache some attributes locally.
        df = self.df
        target = self.target
        bound_type = self.bound_type
        while new_found:
            if self.time_limit is not None and (time.time() - start_time) >= self.time_limit:
                logging.info("Time limit reached. Halting search.")
                break
            new_found = False
            # Loop through complexities.
            for complexity in range(1, self.max_complexity + 1):
                logging.info(f"Generating candidates for complexity level {complexity}...")
                candidates = []
                if complexity == 1:
                    for col in self.candidate_cols:
                        candidates.extend(self._generate_candidates_unary(col))
                elif complexity == 2:
                    for col1 in self.candidate_cols:
                        for col2 in self.candidate_cols:
                            if col1 != col2:
                                candidates.extend(self._generate_candidates_binary(col1, col2))
                # elif complexity == 3:
                    #
                    # candidates.extend(self._generate_candidates_max_of_three())
                    # candidates.extend(self._generate_candidates_min_of_three())
                    # for col1, col2, col3 in combinations(self.candidate_cols, 3):
                    #     candidates.extend(self._generate_candidates_trinary(col1, col2, col3))
                    # Also include linear combinations of 3 terms.
                    # lin_candidates = self._generate_candidates_linear_combination(num_terms=2)
                    # for cand in lin_candidates:
                    #     candidates.extend(self._expand_candidate(cand))
                else:
                    logging.debug("Complexity level not yet implemented.")

                logging.info(f"Generated {len(candidates)} candidates for complexity {complexity}.")
                if not candidates:
                    continue

                with tqdm(total=len(candidates), desc=f"Complexity {complexity}", leave=True) as pbar:
                    for rhs_str, func in candidates:
                        if self.time_limit is not None and (time.time() - start_time) >= self.time_limit:
                            logging.info("Time limit reached during candidate evaluation. Halting search.")
                            new_found = False
                            break
                        try:
                            candidate_series = func(df)
                        except Exception as e:
                            logging.warning(f"Skipping candidate {rhs_str} due to error: {e}")
                            pbar.update(1)
                            continue
                        pbar.set_postfix(candidate=rhs_str)
                        pbar.update(1)
                        if not self._inequality_holds(candidate_series):
                            continue
                        if not self._is_significant(candidate_series):
                            continue
                        logging.info(f"Candidate accepted: {rhs_str}")
                        self._record_conjecture(complexity, rhs_str, func)
                        new_found = True
                        break
                if new_found:
                    break
            if not new_found:
                logging.info("No further significant conjectures found within the maximum complexity.")
                break

    # -------------------- Evaluation Helpers --------------------
    def _inequality_holds(self, candidate_series):
        target_series = self.df[self.target]
        if self.bound_type == 'lower':
            return (target_series >= candidate_series).all()
        else:
            return (target_series <= candidate_series).all()

    def _is_significant(self, candidate_series):
        current_bound = self._compute_current_bound()
        if self.bound_type == 'lower':
            diff = candidate_series - current_bound
        else:
            diff = current_bound - candidate_series
        return (diff > 0).any()

    def _compute_current_bound(self):
        if not self.accepted_conjectures:
            return pd.Series(-np.inf if self.bound_type == 'lower' else np.inf, index=self.df.index)
        bounds = []
        for conj in self.accepted_conjectures:
            try:
                b = conj['func'](self.df)
                bounds.append(b)
            except Exception as e:
                print("Error computing accepted bound:", conj['full_expr_str'], e)
        df_bounds = pd.concat(bounds, axis=1)
        return df_bounds.max(axis=1) if self.bound_type == 'lower' else df_bounds.min(axis=1)

    def _record_conjecture(self, complexity, rhs_str, func):
        if self.hypothesis_str:
            if self.bound_type == 'lower':
                full_expr_str = f"For any {self.hypothesis_str}, {self.target} ≥ {rhs_str}."
            else:
                full_expr_str = f"For any {self.hypothesis_str}, {self.target} ≤ {rhs_str}."
        else:
            full_expr_str = f"{self.target} ≥ {rhs_str}" if self.bound_type == 'lower' else f"{self.target} ≤ {rhs_str}"
        new_conj = {
            'complexity': complexity,
            'rhs_str': rhs_str,
            'full_expr_str': full_expr_str,
            'func': func,
            'bound_type': self.bound_type
        }
        try:
            candidate_series = func(self.df)
        except Exception as e:
            print("Error evaluating candidate during record:", e)
            candidate_series = None
        touches = int((self.df[self.target] == candidate_series).sum()) if candidate_series is not None else 0
        new_conj['touch'] = touches
        self.accepted_conjectures.append(new_conj)
        print(f"Accepted conjecture (complexity {complexity}, touch {touches}): {full_expr_str}")
        self._prune_conjectures()

    def _prune_conjectures(self):
        new_conjectures = []
        removed_conjectures = []
        n = len(self.accepted_conjectures)
        for i in range(n):
            conj_i = self.accepted_conjectures[i]
            try:
                series_i = conj_i['func'](self.df)
            except Exception as e:
                print("Error evaluating conjecture for pruning:", e)
                continue
            dominated = False
            for j in range(n):
                if i == j:
                    continue
                try:
                    series_j = self.accepted_conjectures[j]['func'](self.df)
                except Exception as e:
                    continue
                if self.bound_type == 'lower':
                    if ((series_j >= series_i).all() and (series_j > series_i).any()):
                        dominated = True
                        break
                else:
                    if ((series_j <= series_i).all() and (series_j < series_i).any()):
                        dominated = True
                        break
            if not dominated:
                new_conjectures.append(conj_i)
            else:
                removed_conjectures.append(conj_i)
        if removed_conjectures:
            print("Pruning conjectures:")
            for rem in removed_conjectures:
                print("Removed:", rem['full_expr_str'])
        self.accepted_conjectures = new_conjectures


# # legacy_graffiti.py
# import time
# from functools import partial
# from itertools import combinations, product
# from tqdm import tqdm
# import numpy as np
# import pandas as pd
# import logging
# import pulp
# from fractions import Fraction

# # Import candidate operations.
# from graffitiai.experimental.candidate_operations import (
#     identity_func, square_func, floor_func, ceil_func,
#     add_ratio_func, sub_ratio_func, multiply_ratio_func,
#     add_columns_func, subtract_columns_func, subtract_columns_func_reversed,
#     multiply_columns_func, max_columns_func, min_columns_func,
#     abs_diff_columns_func, safe_division_func, safe_division_func_reversed,
#     mod_func, sqrt_func
# )

# # Import candidate transformations.
# from graffitiai.experimental.candidate_transformations import (
#     floor_transform, ceil_transform,
#     add_ratio_transform, sub_ratio_transform, multiply_ratio_transform,
#     sqrt_transform
# )

# __all__ = ["LegacyGraffiti"]

# logging.basicConfig(
#     level=logging.INFO,  # Set to DEBUG for more detailed output
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# # --- LP Solver Function ---
# def solve_optimal_linear_combination(target, invariants, include_intercept=False):
#     """
#     Solve for coefficients a_i in the candidate expression:
#       E(x) = sum_i a_i * invariants[i](x) [+ b]
#     so that for every row x:
#       target(x) - E(x) >= epsilon,
#     and maximize epsilon.

#     Filters out rows with NaN or infinite values.

#     Returns:
#        coeffs: list of optimal coefficients (floats) (if include_intercept, last element is b)
#        epsilon: optimal margin (float)
#     """
#     pulp.LpSolverDefault.msg = 0
#     # Filter out non-finite rows.
#     mask = np.isfinite(target)
#     for inv in invariants:
#         mask = mask & np.isfinite(inv)
#     if not np.any(mask):
#         return None, None
#     target = target[mask]
#     invariants = [inv[mask] for inv in invariants]

#     n = len(invariants)
#     N = len(target)
#     prob = pulp.LpProblem("OptimalLinearCombination", pulp.LpMaximize)
#     a_vars = [pulp.LpVariable(f"a_{i}", lowBound=None, cat="Continuous") for i in range(n)]
#     if include_intercept:
#         b = pulp.LpVariable("b", lowBound=None, cat="Continuous")
#     epsilon = pulp.LpVariable("epsilon", lowBound=None, cat="Continuous")
#     prob += epsilon, "Maximize minimum margin"
#     for j in range(N):
#         expr = pulp.lpSum(a_vars[i] * invariants[i][j] for i in range(n))
#         if include_intercept:
#             expr += b
#         prob += target[j] - expr >= epsilon, f"row_{j}"
#     prob.solve()
#     if pulp.LpStatus[prob.status] != "Optimal":
#         return None, None
#     coeffs = [pulp.value(var) for var in a_vars]
#     if include_intercept:
#         coeffs.append(pulp.value(b))
#     eps_value = pulp.value(epsilon)
#     return coeffs, eps_value

# # --- LegacyGraffiti Class ---
# class LegacyGraffiti:
#     def __init__(self, df, target_invariant, bound_type='lower', filter_property=None, time_limit=None):
#         self.df_full = df.copy()
#         if filter_property is not None:
#             self.df = df[df[filter_property] == True].copy()
#             self.hypothesis_str = filter_property
#         else:
#             self.df = df.copy()
#             self.hypothesis_str = None

#         self.target = target_invariant
#         self.bound_type = bound_type  # 'lower' or 'upper'
#         self.time_limit = time_limit  # in seconds

#         # Candidate columns: numeric columns (non-boolean) other than the target.
#         self.candidate_cols = [
#             col for col in self.df.columns
#             if col != target_invariant and
#                pd.api.types.is_numeric_dtype(self.df[col]) and
#                not pd.api.types.is_bool_dtype(self.df[col])
#         ]

#         self.accepted_conjectures = []
#         self.max_complexity = 7

#         # List of Fraction ratios.
#         self.ratios = [
#             Fraction(1, 10), Fraction(3, 10), Fraction(7, 10), Fraction(9, 10),
#             Fraction(1, 9), Fraction(2, 9), Fraction(4, 9), Fraction(5, 9),
#             Fraction(7, 9), Fraction(8, 9), Fraction(10, 9),
#             Fraction(1, 8), Fraction(3, 8), Fraction(5, 8), Fraction(7, 8), Fraction(9, 8),
#             Fraction(1, 7), Fraction(2, 7), Fraction(3, 7), Fraction(4, 7), Fraction(5, 7),
#             Fraction(6, 7), Fraction(8, 7), Fraction(9, 7),
#             Fraction(1, 6), Fraction(5, 6), Fraction(7, 6),
#             Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5), Fraction(6, 5),
#             Fraction(7, 5), Fraction(8, 5), Fraction(9, 5),
#             Fraction(1, 4),
#             Fraction(1, 3), Fraction(2, 3), Fraction(4, 3), Fraction(5, 3),
#             Fraction(7, 3), Fraction(8, 3), Fraction(10, 3),
#             Fraction(1, 2), Fraction(3, 2), Fraction(5, 2), Fraction(7, 2), Fraction(9, 2),
#             Fraction(1, 1), Fraction(2, 1), Fraction(3, 1), Fraction(4, 1),
#         ]

#     # -------------------- Candidate Generation Methods --------------------
#     def _generate_candidates_unary(self, col):
#         base = [
#             (f"{col}", partial(identity_func, col=col)),
#             (f"({col})^2", partial(square_func, col=col)),
#             (f"floor({col})", partial(floor_func, col=col)),
#             (f"ceil({col})", partial(ceil_func, col=col))
#         ]
#         mult_candidates = [(f"{col} * {ratio}", partial(multiply_ratio_func, col=col, ratio=ratio))
#                            for ratio in self.ratios]
#         add_candidates = [(f"({col}) + {ratio}", partial(add_ratio_func, col=col, ratio=ratio))
#                           for ratio in self.ratios]
#         sub_candidates = [(f"({col}) - {ratio}", partial(sub_ratio_func, col=col, ratio=ratio))
#                           for ratio in self.ratios]
#         return base + mult_candidates + add_candidates + sub_candidates

#     def _generate_candidates_binary(self, col1, col2):
#         candidates = [
#             (f"({col1} + {col2})", partial(add_columns_func, col1=col1, col2=col2)),
#             (f"({col1} - {col2})", partial(subtract_columns_func, col1=col1, col2=col2)),
#             (f"({col2} - {col1})", partial(subtract_columns_func_reversed, col1=col1, col2=col2)),
#             (f"{col1} * {col2}", partial(multiply_columns_func, col1=col1, col2=col2)),
#             (f"max({col1}, {col2})", partial(max_columns_func, col1=col1, col2=col2)),
#             (f"min({col1}, {col2})", partial(min_columns_func, col1=col1, col2=col2)),
#             (f"abs({col1} - {col2})", partial(abs_diff_columns_func, col1=col1, col2=col2)),
#             (f"{col1}*{col2}", partial(multiply_columns_func, col1=col1, col2=col2))
#         ]
#         if (self.df[col2] == 0).sum() == 0:
#             candidates.append((f"({col1} / {col2})", partial(safe_division_func, col1=col1, col2=col2)))
#         if (self.df[col1] == 0).sum() == 0:
#             candidates.append((f"({col2} / {col1})", partial(safe_division_func_reversed, col1=col1, col2=col2)))
#         candidates.append((f"({col1} mod {col2})", partial(mod_func, col1=col1, col2=col2)))
#         return candidates

#     def _generate_candidates_complex_mod_sqrt(self):
#         candidates = []
#         for a, n, d in combinations(self.candidate_cols, 3):
#             def candidate_func(df, a=a, n=n, d=d):
#                 mod_val = mod_func(df, n, d)
#                 one_plus = 1 + mod_val
#                 product_val = df[a] * one_plus
#                 sqrt_val = np.sqrt(product_val)
#                 return np.ceil(sqrt_val)
#             expr_str = f"CEIL(sqrt({a} * (1 + ({n} mod {d}))))"
#             candidates.append((expr_str, candidate_func))
#         return candidates

#     def _generate_candidates_linear_combination_optimal(self, candidate_columns, num_terms, include_intercept=False):
#         invariants = [self.df[col].values for col in candidate_columns]
#         target_vals = self.df[self.target].values
#         coeffs, eps = solve_optimal_linear_combination(target_vals, invariants, include_intercept=include_intercept)
#         if coeffs is None or eps is None or eps <= 0:
#             return None
#         if include_intercept:
#             frac_coeffs = [Fraction(c).limit_denominator() for c in coeffs[:-1]]
#             intercept = Fraction(coeffs[-1]).limit_denominator()
#         else:
#             frac_coeffs = [Fraction(c).limit_denominator() for c in coeffs]
#         expr_parts = []
#         for col, frac in zip(candidate_columns, frac_coeffs):
#             if frac != 0:
#                 expr_parts.append(f"{frac}*({col})")
#         if include_intercept:
#             expr_parts.append(f"{intercept}")
#         candidate_expr = " + ".join(expr_parts)
#         def candidate_func(df):
#             total = 0
#             for col, c in zip(candidate_columns, coeffs[:-1] if include_intercept else coeffs):
#                 total += c * df[col]
#             if include_intercept:
#                 total += coeffs[-1]
#             return total
#         return candidate_expr, candidate_func

#     # -------------------- Candidate Transformations --------------------
#     def _with_floor_ceil(self, candidate):
#         base_rhs, base_func = candidate
#         return [(f"floor({base_rhs})", partial(floor_transform, base_func=base_func)),
#                 (f"ceil({base_rhs})", partial(ceil_transform, base_func=base_func))]

#     def _with_ratio_addition(self, candidate):
#         base_rhs, base_func = candidate
#         return [(f"({base_rhs}) + {ratio}", partial(add_ratio_transform, base_func=base_func, ratio=ratio))
#                 for ratio in self.ratios]

#     def _with_ratio_subtraction(self, candidate):
#         base_rhs, base_func = candidate
#         return [(f"({base_rhs}) - {ratio}", partial(sub_ratio_transform, base_func=base_func, ratio=ratio))
#                 for ratio in self.ratios]

#     def _with_ratio_multiplication(self, candidate):
#         base_rhs, base_func = candidate
#         return [(f"{ratio}*({base_rhs})", partial(multiply_ratio_transform, base_func=base_func, ratio=ratio))
#                 for ratio in self.ratios]

#     def _expand_candidate(self, candidate):
#         variants = {candidate[0]: candidate}
#         for transform_func in [self._with_floor_ceil, self._with_ratio_multiplication,
#                                self._with_ratio_subtraction, self._with_ratio_addition]:
#             for cand in transform_func(candidate):
#                 variants.setdefault(cand[0], cand)
#         return list(variants.values())

#     # -------------------- Search Loop --------------------
#     def search(self):
#         start_time = time.time()
#         new_found = True
#         logging.info("Starting the search process...")
#         df = self.df
#         if self.time_limit is not None and (time.time() - start_time) >= self.time_limit:
#             logging.info("Time limit reached. Halting search.")
#             return
#         while new_found:
#             if self.time_limit is not None and (time.time() - start_time) >= self.time_limit:
#                 logging.info("Time limit reached. Halting search.")
#                 break
#             new_found = False
#             for complexity in range(1, self.max_complexity + 1):
#                 logging.info(f"Generating candidates for complexity {complexity}...")
#                 candidates = []
#                 if complexity == 1:
#                     # LP-based candidate for each column with intercept
#                     for col in self.candidate_cols:
#                         lp_candidate = self._generate_candidates_linear_combination_optimal((col,), 1, include_intercept=True)
#                         if lp_candidate is not None:
#                             candidates.append(lp_candidate)
#                     # Enumerated unary candidates.
#                     for col in self.candidate_cols:
#                         candidates.extend(self._generate_candidates_unary(col))
#                 elif complexity == 2:
#                     # For each pair, add LP-based candidate (with intercept)
#                     for combo in combinations(self.candidate_cols, 2):
#                         lp_candidate = self._generate_candidates_linear_combination_optimal(combo, 2, include_intercept=True)
#                         if lp_candidate is not None:
#                             candidates.append(lp_candidate)
#                     # Also add enumerated binary candidates.
#                     for col1, col2 in combinations(self.candidate_cols, 2):
#                         candidates.extend(self._generate_candidates_binary(col1, col2))
#                 elif complexity == 3:
#                     # Include mod-sqrt candidates.
#                     candidates.extend(self._generate_candidates_complex_mod_sqrt())
#                     # And LP-based candidates for triplets.
#                     for combo in combinations(self.candidate_cols, 3):
#                         lp_candidate = self._generate_candidates_linear_combination_optimal(combo, 3, include_intercept=True)
#                         if lp_candidate is not None:
#                             candidates.append(lp_candidate)
#                 else:
#                     logging.debug("Complexity level not yet implemented.")
#                 logging.info(f"Generated {len(candidates)} candidates for complexity {complexity}.")
#                 if not candidates:
#                     continue
#                 with tqdm(total=len(candidates), desc=f"Complexity {complexity}", leave=True) as pbar:
#                     for rhs_str, func in candidates:
#                         if self.time_limit is not None and (time.time() - start_time) >= self.time_limit:
#                             logging.info("Time limit reached during candidate evaluation. Halting search.")
#                             new_found = False
#                             break
#                         try:
#                             candidate_series = func(df)
#                         except Exception as e:
#                             logging.warning(f"Skipping candidate {rhs_str} due to error: {e}")
#                             pbar.update(1)
#                             continue
#                         pbar.set_postfix(candidate=rhs_str)
#                         pbar.update(1)
#                         if not self._inequality_holds(candidate_series):
#                             continue
#                         if not self._is_significant(candidate_series):
#                             continue
#                         logging.info(f"Candidate accepted: {rhs_str}")
#                         self._record_conjecture(complexity, rhs_str, func)
#                         new_found = True
#                         break
#                 if new_found:
#                     break
#             if not new_found:
#                 logging.info("No further significant conjectures found within the maximum complexity.")
#                 break

#     # -------------------- Evaluation Helpers --------------------
#     def _inequality_holds(self, candidate_series):
#         target_series = self.df[self.target]
#         if self.bound_type == 'lower':
#             return (target_series >= candidate_series).all()
#         else:
#             return (target_series <= candidate_series).all()

#     def _is_significant(self, candidate_series):
#         current_bound = self._compute_current_bound()
#         if self.bound_type == 'lower':
#             diff = candidate_series - current_bound
#         else:
#             diff = current_bound - candidate_series
#         return (diff > 0).any()

#     def _compute_current_bound(self):
#         if not self.accepted_conjectures:
#             return pd.Series(-np.inf if self.bound_type == 'lower' else np.inf, index=self.df.index)
#         bounds = []
#         for conj in self.accepted_conjectures:
#             try:
#                 b = conj['func'](self.df)
#                 bounds.append(b)
#             except Exception as e:
#                 print("Error computing accepted bound:", conj['full_expr_str'], e)
#         df_bounds = pd.concat(bounds, axis=1)
#         return df_bounds.max(axis=1) if self.bound_type == 'lower' else df_bounds.min(axis=1)

#     def _record_conjecture(self, complexity, rhs_str, func):
#         if self.hypothesis_str:
#             if self.bound_type == 'lower':
#                 full_expr_str = f"For any {self.hypothesis_str}, {self.target} ≥ {rhs_str}."
#             else:
#                 full_expr_str = f"For any {self.hypothesis_str}, {self.target} ≤ {rhs_str}."
#         else:
#             full_expr_str = f"{self.target} ≥ {rhs_str}" if self.bound_type == 'lower' else f"{self.target} ≤ {rhs_str}"
#         new_conj = {
#             'complexity': complexity,
#             'rhs_str': rhs_str,
#             'full_expr_str': full_expr_str,
#             'func': func,
#             'bound_type': self.bound_type
#         }
#         try:
#             candidate_series = func(self.df)
#         except Exception as e:
#             print("Error evaluating candidate during record:", e)
#             candidate_series = None
#         touches = int((self.df[self.target] == candidate_series).sum()) if candidate_series is not None else 0
#         new_conj['touch'] = touches
#         self.accepted_conjectures.append(new_conj)
#         print(f"Accepted conjecture (complexity {complexity}, touch {touches}): {full_expr_str}")
#         self._prune_conjectures()

#     def _prune_conjectures(self):
#         new_conjectures = []
#         removed_conjectures = []
#         n = len(self.accepted_conjectures)
#         for i in range(n):
#             conj_i = self.accepted_conjectures[i]
#             try:
#                 series_i = conj_i['func'](self.df)
#             except Exception as e:
#                 print("Error evaluating conjecture for pruning:", e)
#                 continue
#             dominated = False
#             for j in range(n):
#                 if i == j:
#                     continue
#                 try:
#                     series_j = self.accepted_conjectures[j]['func'](self.df)
#                 except Exception as e:
#                     continue
#                 if self.bound_type == 'lower':
#                     if ((series_j >= series_i).all() and (series_j > series_i).any()):
#                         dominated = True
#                         break
#                 else:
#                     if ((series_j <= series_i).all() and (series_j < series_i).any()):
#                         dominated = True
#                         break
#             if not dominated:
#                 new_conjectures.append(conj_i)
#             else:
#                 removed_conjectures.append(conj_i)
#         if removed_conjectures:
#             print("Pruning conjectures:")
#             for rem in removed_conjectures:
#                 print("Removed:", rem['full_expr_str'])
#         self.accepted_conjectures = new_conjectures
