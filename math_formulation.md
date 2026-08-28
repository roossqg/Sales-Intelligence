# 1. Product x Price optimization:

## Mathematical Formulation

The objective is to determine the optimal quantity of each product in order to maximize total profit while respecting budget and capacity constraints.

### Decision Variables

For each product $i$:

$$
q_i = \text{quantity of product } i
$$

where:

$$
q_i \in \mathbb{Z}_{\geq 0}
$$

### Parameters

For each product $i$:

- $p_i$: selling price per unit
- $c_i$: cost per unit
- $w_i$: capacity consumed per unit
- $B$: available budget
- $C_i$: total available capacity per product

The unit profit of product $i$ is:

$$
\pi_i = p_i - c_i
$$

### Objective Function

The objective is to maximize total profit:

$$
\max Z =
\sum_{i=1}^{n}(p_i-c_i)q_i
$$

or equivalently:

$$
\max Z =
\sum_{i=1}^{n}p_iq_i
-
\sum_{i=1}^{n}c_iq_i
$$

### Constraints

#### Budget Constraint

The total cost cannot exceed the available budget:

$$
\sum_{i=1}^{n}c_iq_i \leq B
$$

#### Capacity Constraint

The total capacity consumed cannot exceed the available capacity for each product/class:

$$
\sum_{i=1}^{n}w_iq_i \leq C_i
$$

#### Non-Negativity and Integrality

The quantity of each product must be a non-negative integer:

$$
q_i \in \mathbb{Z}_{\geq 0}
$$

### Complete Optimization Model

The complete model can be written as:

$$
\begin{aligned}
\max_{q_1,\ldots,q_n}
\quad & \sum_{i=1}^{n}(p_i-c_i)q_i \\[4pt]
\text{subject to}
\quad & \sum_{i=1}^{n}c_iq_i \leq B \\[4pt]
& \sum_{i=1}^{n}w_iq_i \leq C_i \\[4pt]
& q_i \in \mathbb{Z}_{\geq 0},
\qquad i=1,\ldots,n
\end{aligned}
$$

### Problem Classification

This is an **Integer Linear Programming (ILP)** problem because:

- The decision variables are integers.
- The objective function is linear.
- All constraints are linear.

If the variables were allowed to take continuous values instead of integer values, the problem would be a standard **Linear Programming (LP)** problem.

---

# 2. Forecasting

## 1. Problem Definition

Given a historical time series of sales observations, the objective is to forecast future revenue values based exclusively on the temporal structure of the observed series.

Let

$$
y_t = \text{revenue at time } t
$$

where

$$
t = 1,2,\ldots,T.
$$

Given the historical observations

$$
\mathcal{Y}_T = {y_1,y_2,\ldots,y_T},
$$

the objective is to estimate future values

$$
\hat{y}*{T+1},\hat{y}*{T+2},\ldots,\hat{y}_{T+h},
$$

where $h$ is the forecasting horizon.

---

## 2. ARIMA Model

The ARIMA model is defined by three parameters:

$$
ARIMA(p,d,q)
$$

where:

* $p$: autoregressive order;
* $d$: order of differencing;
* $q$: moving-average order.

The model first transforms the original series through differencing:

$$
y_t^{(d)} = (1-B)^d y_t
$$

where $B$ is the backshift operator:

$$
By_t = y_{t-1}.
$$

After differencing, the resulting stationary series is modeled using an ARMA($p,q$) process.


## 3. Dataset Structure

A generic sales dataset can be represented as:

| datetime | revenue |
| -------- | -------: |
| $t_1$    |    $y_1$ |
| $t_2$    |    $y_2$ |
| $\vdots$ | $\vdots$ |
| $t_T$    |    $y_T$ |

The `datetime` variable defines the temporal index, while `revenue` represents the target variable.

If the original dataset contains individual transactions, the observations should first be aggregated into the desired forecasting frequency:

$$
y_t =
\sum_{i \in \mathcal{T}_t} revenue_i
$$

where $\mathcal{T}_t$ represents total revenue occurring during period $t$.

Examples of forecasting frequency include:

* Daily revenue;
* Weekly revenue;
* Monthly revenue.


## 8. Model Selection

The ARIMA orders are represented by:

$$
(p,d,q).
$$

A practical model-selection procedure is:

1. Analyze the original revenue series;
2. Determine whether differencing is necessary;
3. Select candidate values for $p$ and $q$;
4. Fit candidate ARIMA models;
5. Compare models using information criteria such as AIC/BIC;
6. Evaluate forecasting performance on a temporal validation set;
7. Analyze the residuals.

The selected model can therefore be represented as:

$$
ARIMA(p^*,d^*,q^*)
$$

where $(p^*,d^*,q^*)$ is the chosen configuration.

---

## 10. Final Forecasting Problem

The complete forecasting problem can therefore be summarized as:

$$
\boxed{
\hat{y}_{T+h}
=============

f_{\text{ARIMA}}
\left(
y_1,\ldots,y_T;
p,d,q
\right)
}
$$

for

$$
h=1,\ldots,H.
$$

The goal is to construct an ARIMA model capable of accurately predicting future revenue while adequately representing the temporal dependencies present in the historical sales series.

