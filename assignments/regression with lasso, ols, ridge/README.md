# Regression Model Comparison – Ames Housing Dataset

This project compares **Ordinary Least Squares (OLS)**, **Lasso Regression**, and **Ridge Regression** on the Ames Housing dataset.  
The main goal was to evaluate their performance, understand the effect of regularization, and compare feature importance.

---

## 📊 Model Performance

| Model  | RMSE       | MAE       | R²      | Notes |
|--------|-----------:|----------:|--------:|-------|
| **OLS (Linear Regression)**  | 360,967 | 270,427 | -17.03 | 🚨 Performed very poorly, worse than predicting the mean. Highly sensitive to outliers and multicollinearity. |
| **Lasso Regression (L1)**    | 66,760  | 53,347  | 0.38   | 👍 Better than OLS. Performs feature selection by shrinking some coefficients to **0**, but dropped too many useful features → limited performance. |
| **Ridge Regression (L2)**    | 38,281  | 30,920  | 0.80   | 🏆 Best performer. Keeps all features but shrinks them proportionally, leading to strong generalization and robustness against outliers. |

---

## ⚖️ Key Takeaways
1. **OLS** failed because it included every feature, making it very sensitive to noise.  
2. **Lasso** helped by performing automatic feature selection, but over-shrank important predictors.  
3. **Ridge** struck the best balance — keeping all features, but reducing overfitting via coefficient shrinkage.  

---

## 📌 Regularization Intuition
- **L1 (Lasso)**: Some coefficients → 0 (feature selection).  
- **L2 (Ridge)**: All coefficients reduced but none are eliminated.  
- **OLS**: No penalty, fits data exactly (prone to overfitting).  

---

## 🔮 Next Steps
- Try **ElasticNet (L1 + L2 mix)** for a balance between Ridge & Lasso.  
- Perform **feature importance analysis** (compare coefficients).  
- Add **visualizations**:  
  - Actual vs Predicted plots  
  - Error distribution  
  - Coefficient shrinkage comparison  

---
