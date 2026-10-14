# FRE-GT-9743 Assignment 4

Chuyu Wu

## Written question: Futures settlement and OTC collateral

Daily cash transfers can look similar, but they do different jobs. For a collateralized OTC forward or swap, collateral secures the amount owed; it does not normally discharge the derivative's future payment. The collateral is returned or applied when the trade is settled, and cash collateral usually earns interest under the CSA. The remaining future cashflows therefore still have a present value. Under ideal full cash collateralization, the collateral remuneration rate determines the discounting rate.

For example, if a forward's terminal payoff is $S_T-K$, its value is
$$V_t=E_t^Q[D(t,T)(S_T-K)].$$
The delivery price that makes a new forward worth zero is
$$K_t=\frac{E_t^Q[D(t,T)S_T]}{E_t^Q[D(t,T)]}.$$
Posting collateral against this value does not turn the terminal payoff into a payment received today.

For a futures contract, variation settlement actually pays out the day's gain or loss. If the futures price rises from 100 to 103, the long receives 3 per unit now, and the contract resets to zero value at 103. That 3 is already settled profit rather than refundable security for a later payment. Initial margin is separate: it protects against potential future losses.

Under the assignment's assumption that the next period's interest rate is known at the start of that period,
$$0=E_{t_k}^Q[D(t_k,t_{k+1})(F_{k+1}-F_k)]
 =D(t_k,t_{k+1})(E_{t_k}^Q[F_{k+1}]-F_k).$$
The same known, positive discount factor multiplies both terms, so it cancels. Thus $F_k=E_{t_k}^Q[F_{k+1}]$ and, by iteration, $F_k=E_{t_k}^Q[S_T]$. Discounting has been used in the argument; it disappears from the futures-price recursion because the gain is settled each day.

The distinction is the contract's settlement and interest terms, rather than simply OTC versus exchange trading. Some cleared OTC swaps also use settled-to-market treatment, with price-alignment payments. Also, if the next-period discount factor is random, the cancellation step above cannot simply be assumed; the assignment's result uses its stated short-period assumption. With deterministic rates over the whole life, forward and futures delivery prices coincide.

Sources consulted: [CME: Money Calculations for Futures and Options](https://www.cmegroup.com/education/articles-and-reports/money-calculations-for-futures-and-options); [LCH filing on collateralized-to-market and settled-to-market swaps](https://www.sec.gov/Archives/edgar/data/1114446/000111444616011435/filename1.htm).
