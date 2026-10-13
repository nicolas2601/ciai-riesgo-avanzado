# Benchmark (validation)

| model | macro-F1 | bal_acc | accuracy | status |
|---|---|---|---|---|
| A_dummy_majority | 0.3249 | 0.3333 | 0.9505 | evaluated |
| B_logreg_balanced | 0.5253 | 0.6759 | 0.7887 | evaluated |
| C_ros_logreg | 0.5113 | 0.6817 | 0.779 | evaluated |
| D_smote_logreg | 0.5367 | 0.6914 | 0.8329 | evaluated |
| E_rf_balanced | 0.5933 | 0.6188 | 0.9576 | evaluated |

Selection: highest val macro_f1 -> **E_rf_balanced** (ties: balanced accuracy, then simpler model).
