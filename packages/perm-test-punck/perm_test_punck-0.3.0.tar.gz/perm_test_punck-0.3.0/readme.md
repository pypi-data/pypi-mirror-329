# perm test
A rust implementation of comparative permutation testing, because python is not that fast

Input example: ` perm_test.test(amount, group_1, group_2) `.

Output of type: `p_value, [tstats of permutations]`.

Can also return a single tstat if called with `perm_test.test(group_1, group_2)`.

Only one dimensional datasets have been implemented.
