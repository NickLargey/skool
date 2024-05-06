## Class Goals:  
- Solve $Ax = b$ where A is a matrix and x, b are vectors without finding $A^{-1}$ $$Ax = b ==> x = A^{-1}b$$  
- NEVER CALCULATE THE INVERSE OF A MATRIX  
  
## Topics:  
1. Julia Primer  
2. Linear Algebra Primer  
3. Understanding error  
1. Floating Point Number System IEEE-754  
2. Alternative representations of floating point number systems for Deep Learning  
1. Google's bfloat-16  
2. Posit - John Gustafston  
4. Direct Methods for solving $Ax = b$  
5. Least Squares Approximation  
6. Indirect Methods/Iterative Methods  
1. 2 or 3 stationary methods  
2. 1 Non-stationary method (Gradient Descent)  
  
## 1/23/2024  
  
- MatLab - Matrix Laboratory  
- **Everything** is a matrix  
- 'a' --> \[a] -> 1 x 1 matrix  
- \[1,2,3] --> \[1,2,3] -> 1 x 3 matrix  
  
- Vectors are always considered column matrices  
$$ y =\begin{bmatrix} x_{1} \\ x_{2} \\ \vdots \\ x_{m} \end{bmatrix} $$  
- Tchebyshev Nodes:  
![[ChebyshevNodes.jpg]]  
  
$$ \cos . (0:n) * (\pi/n) $$  
-1 -|-|-|-|-|-|-|-|-|-|- 1 --> equally spaced number line from -1:1  
- Julia syntax `-1:0.1:`  
- Better: `collect(-1:0.1:1)`  
  
### 1/30/2024  
  
Slicing/Subsetting (Submatrix)  
  
- $A = \begin{bmatrix} 1 & 2 & 3 & 4 \\ 5 & 6 & 7 & 8 \\ 9 & 10 & 11 & 12 \\ 13 & 14 & 15 & 16\end{bmatrix}$  
  
- Using colon ( : ) operator  
- A\[2,3] --> \[7]  
- A\[3, : ] --> \[9,10,11,12]  
- A\[:, 2] --> 2nd column  
- A\[ :, end] --> last row  
- A\[\[2,3], : ] --> Rows 2 and 3  
  
### 2/1/2024  
Timing code:  
- @time  
- @timev  
- @ elapsed  
  
Benchmarking Package --> Stochastic Benchmarking runs multiple iterations, normalizes run times and returns a range  
  
Algebra - a Set (real numbers) with operations (+, x) and properties (Commutative, Associative, Distributive, etc...).  
  
Scalar Multiplication - Any vector can be multiplied by a constant  
$V=\begin{bmatrix}3 \\ -2 \\ 5\end{bmatrix}$ $3V=\begin{bmatrix}9 \\ -6 \\ 15\end{bmatrix}$  
  
$V_1 + V_2 = $\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix} + \begin{bmatrix}4 \\ 5 \\ 6\end{bmatrix}$ >>> Transpose one vector $V=\begin{bmatrix}1 \\ 2 \\ 3\end{bmatrix} + [4, 5, 6] = \begin{bmatrix}5 \\ 7 \\ 9\end{bmatrix}$  
$X, y \in R^n$  
Vector Norm (distance in length from the origin) --> $3 \in R^1 = \vert{3}\vert$ called the Euclidian norm  
  
$X \in R^3 = \begin{bmatrix}x_1 \\ x_2 \\ x_3\end{bmatrix}$ we will use $\vert x \vert _p = \sqrt[p]{\epsilon{\vert x \vert}^p}$  
## 2/6/2024  
  
Linear Algebra  
- Vector Norm  
- A measurement of the "distance" from zero.  
- Analog to the absolute value  
- In our use case we will be using it to take the norm of 2 different vectors i.e. || x - y ||  
- How to Calculate:  
- 1-Norm >> $||x||_1$ >> $\sum^n_{i=1} | x_i|$  
- 2-Norm >> $||x||_2$ >> $\sqrt{x_1^2 + x_2^2 + ... + x_n^2}$  
- Infinity Norm or Max Norm >> $||x||_{\infty}$ >> $max(|x_1|, |x_1|, |x_1| ... |x_n|,)$  
- Matrix Multiplication  
- Theorem: Matrix Representation Theorem: Every linear transformation has a Matrix representation  
  
- $\begin{bmatrix}1 & 2\\ 3 & 4 \end{bmatrix}$  $\begin{bmatrix}5\\ 6 \end{bmatrix}$ = $\begin{bmatrix}1 x 5 + 2 x 6\\ 3 x 5 + 4 x 5 \end{bmatrix}$ = $\begin{bmatrix} 17\\ 39 \end{bmatrix}$  
  
- $\begin{bmatrix}1 & 2\\ 3 & 4 \end{bmatrix}$$\begin{bmatrix}2 & 1\\ 1 & 3 \end{bmatrix}$ = $\begin{bmatrix}4 & 7\\ 10 & 15 \end{bmatrix}$  
  
- MatMul Procedure: $Ax = b$ A and b are given, solve for x. A is a matrix, x and b are vectors.  
-  $A = [a_1\ a_2]$  
- $a_1 = \begin{bmatrix}1 \\ 3 \end{bmatrix}$  
- $a_2 = \begin{bmatrix}2 \\ 4 \end{bmatrix}$  
  
-  $\begin{bmatrix}1 & 2\\ 3 & 4 \end{bmatrix}$$\begin{bmatrix}5\\ 6\end{bmatrix}$  
  
- Linear Combination: $5\begin{bmatrix}1 \\ 3 \end{bmatrix} + 6\begin{bmatrix} 2\\ 4 \end{bmatrix}$ = $\begin{bmatrix}17\\ 39 \end{bmatrix} \epsilon R^2$  
- $A^{-1}$ exists  
1. Compute Inverse  
2. Compute determinant:  
- det(A) does not equal 0  
- det: $R^{an} = R$  
3. if columns of A are independent  
## 2/8/2024  
### Understanding Error and Finite Precision Computation  
  
Sources of error (broadly speaking):  
- Data Error - **Not Class Focus**  
- Measurement Error (incorrect calculations, data noise from transmission)  
- Missing Data  
- Typos  
- Computation Error **Class Focus**-  
1.  Discretization Error:  
- replace the continuous with discrete.  
- $f(x) -> f'(x) \approx f(x + h) - f(x)/h = slope$ or $x^2 -> 2x \approx (x + h)^2 - x^2/h$  
2. Truncation Error:  
- Replacing infinite "process" with a finite process.  
- e.g. Taylor Series: $e^x = 1 + x + x^2/2 + .... -> \int_a^b f(x) dx \approx \sum_{i=1}^{10} f(x) \Delta x_i$  
3. Round-Off Error:  
- By representing numbers in finite precision.  
- $\pi = 3.14$ or $e \approx 0.0015926535...$  
  
- How to deal with errors:  
- Control error  
- Definition of a well-posed problem:  
- Solution exists  
- Unique  
- Small Changes in input result in small changes in output  
  
- Measure Error ($\hat{x}$ = a computed value)  
- Absolute Error: $E_{abs} = |x - \hat{x}|$  
- Relative Error: $E_{rel} = {x - \hat{x}\over{x}}$ **(Pick this one)**  
  
- How do you find "x":  
- Find the bounds on the error:  
- $y - \hat{y}$ --> Forward error  
- $x - \hat{x}$ --> Backwards error  
- ![[20240208_102453.jpg|400]]  
  
- $K_{abs} = {|f(\hat{x}) - f(x)| \over{|\hat{x} - x|}} = {|\Delta{y}| \over{|\Delta{x}|}} \approx f'(\hat{x})$  
- $K_{rel} = {|\Delta{y} / y| \over{|\Delta{x} / x|}} ... \approx \vert{{xf'(x) \over{f(x)}}}\vert$ (on Pg. 51)  
  
## 2/13/2024  
- **Convergence**  
  
- Many of our methods are iterative (e.g. for loop or while loop)  
- Iteration produces a sequence of approximations  
- Ideally this sequence of approximations converges to the exact solution  
- $\alpha_n \to \alpha$  
- A sequence of approximations produces a sequence of errors:  
- ${e_1, e_2, e_3,..... e_n}\ where\ e_j = \vert{\alpha_j - \alpha}\vert$  
  
- Definition of Big-O **NOT THE TIME COMPLEXITY ONE**  
- $f(n) = O(g(n))$ if there exists a constant ($R^+$) : $\vert{f(n)}\vert \le\ C\vert{g(n)}\vert$  
- Definition: Let $\lim_{\alpha_n\to \alpha} \land \beta_n \to 0$, then $\alpha_n$ converges with the **rate of convergence** $O(\beta_n)$  
- $\beta_n$ is used for comparison purposes and is known, often $\beta_n = n^{-p} = {1\over n^p}\ where\ p \gt 1$ and ${1\over n^p} \to 0$  
  
 *Example*  
$a_n = {n + 1\over n+2}\ where\ n = 1,2,3,...$  
Questions to ask:  
1. Does it converge? *Yes*  
2. What's it converge to? *1*  
3. What is its rate of convergence if it does converge? Use $\alpha_n - \alpha$ --> $\vert{{n + 1\over n+2} - 1}\vert = \vert{{n + 1\over n+2} - {n + 2\over n+2}}\vert = \vert{{-1\over n+2}}\vert = \vert{{1\over n+2}}\vert \le \vert{{1\over n}}\vert$  
  
## 2/15/2024  
  
- Big-O $\vert f(n)\vert\  \epsilon O(g(n))\ iff\ \exists\ C\ \land N\ :  \vert f(n)\vert \le\ C\vert g(n)\vert$  
- Not the time Complexity Big-O  
- $\{\alpha\}^\inf_{n=1}$ = Sequence of approximations (an iteration (for-loop))  
- $\alpha\ E\ R$ = exact value  
- $\alpha_n \to \alpha\ as\ n\to \inf\ == \lim_{n\to inf} \alpha_n\ = \alpha$    
- sequence of approximations gives rise to sequence of errors:  
- $e_n\ =\ \alpha_n\ -\ \alpha$  
- $f(n) = \{e_1\ =\ \alpha_1\ -\ \alpha, e_2\ =\ \alpha_2\ -\ \alpha, e_3\ =\ \alpha_3\ -\ \alpha,...\}$  
-  Goal is to bound the errors (i.e. f(n)) by a sequence that we know (i.e. g(n))  
- **Almost Always $$1\over n^p$$  
- $\alpha_n =  {2n^2 + 4n\over n^2+2n +1}$  
- Does $\alpha_n$ converge? *Refresh L'Hopital's rule*  
- if it does, what does it converge to? Converges to 2  
- How Fast? What is the rate of convergence?  
- $$f(n)\ =\ \vert{{2n^2 + 4n\over n^2+2n +1} - 2}\vert$$  
- $${2n^2 +4n - 2(n^2+2n+1)\over n^2 + 2n + 1} = {-2\over n^2 + 2n +1}$$  
- $${2\over n^2 + 2n +1} = 2({1\over n^2 + 2n +1}) \le 2({1\over n^2})\ \exists\ O({1\over n^2})$$  
- C = 2, N = 1  
  
- **Taylor's Theorem**  
- $$f(x) = f(0) + f'(0)x + {f''(0)x^2\over 2} + ... = \sum_{n=0}^\infty {f^n (a)\over n!}(x-a)^n$$  
## 2/22/2024  
  
### 2.2 Scientific Arithmetic  
  
**Mantissa** now called the **Significand**  
  
Significant digits (SigDig): all digits excluding leading zeros  
ex.    1.2345 -> 5 SigDigs  
1.2340 -> still 5 SigDigs  
  
- $100\pi = 3.1416$ to 5 SigDig  
**Def:** Floating-point numbers  
- **F** is floating-point number system with base $\beta$ > 1  
$x \in F, x = \pm\ m \beta^E$  
ex. $(m = 1.234) * (\beta = 10)^{(E = 3)} = 1.234 * 10^3$  
Where $L\ \le E\ \le\ U$ and $m = \sum_{j=0}^{p-1} d_j \beta^{-j}$  
Where p = precision.  
$0 \le d_j \lt \beta, 0 \le d_j \le \beta -1,\ where\ d_j = digits$  
  
$e\ \approx\ 2.7183$  
  
$x = \pm\ m \beta^E \to 2.7183\ (e)\ in\ base\ 2$  
  
$E\ =\ \lfloor log_2 2.7183 \rfloor$  
$2 \% 2 = 1$  
  
Pg. 62  
  
Definition:  
Overflow: any number larger than what is able to be represented is represented as infinity  
Underflow: Any number smaller than what is able to be represented is represented as zero  
Subnormal:  
Underflow Level (UFL): Minimum significand  
$UFL = m_min \beta^L$  
Overflow Level (OFL): Maximum significand  
$OFL = \beta^{U+1}(1- \beta^{-p})$  
  
Machine Precision:  
$fl(x) - x \over x$  
  
## 2/29/2024 - Chapter 3  
  
Solving Systems of Linear Equations:  
- Once again Ax = b $A \in R^{nxn}, b \in R^n, x \in R^n$  
- A is invertible and $A^{-1} exists$  
Def:  
**Dense Matrices**: Most entries are not zeros  
**Sparse Matrices**: Most entries are zeros  
  
- Solve for x:  
- $x = A^{-1}b$  
- Rule #1: Don't compute $A^{-1}$ :  
- Too computationally expensive  
- *Could be* unstable  
- Rule #2:  
  
- Solving for Ax = b:  
- Are there easy cases to find a solution?  
- If so, can we generalize?  
- Triangular systems ARE easy:  
1. Diagonal:  
Only non-zero entries are on the diagonal  
Def: $A_{ij}\ =\ 0\ \forall\ i\ \ne\ j$  
![[20240229_100744.jpg|400]]  
`for i = 1:n x[i] = b[i]/a[i][i]` Can be Parallelized  
2. Lower Triangular:  
Only non-zero entries are in the lower triangle with the diagonal included  
Def: $L\ =\ (l{ij})\ is\ lower\ triangle\ if\ l_{ij}\ =\ 0\ \forall\ i<j$  
3. Upper Triangular:  
Only non-zero entries are in the upper triangle with the diagonal included  
Def: $U\ =\ (u{ij})\ is\ lower\ triangle\ if\ l_{ij}\ =\ 0\ \forall\ i>j$  
  
Forward Substitution:  
![[20240229_100744 1.jpg|400]]  
  
```  
for i=1:n  
 x[i] = b[i] - sum(a[i][j]*x[j]  
 x[i] = x[i]/a[i][i]  
end  
for i=1:n  
 s = 0  
 for j = 1:i-1  
   s = s + a[i][j]*x[j]  
 end  
 x[i] = (b[i] - s)/a[i][i]  
```  
  
  
### 3/5/2024 - Chapter 3 (cont.)  
  
Indirect methods are Iterative  
- Triangular systems (i.e A is triangular) are very computationally efficient  
- Diagonal, $a_{ij}\ =\ 0\ \forall\ i\ \ne\ j$, off diagonal entries = 0  
- Lower Triangular, $a_{ij}\ =\ 0,\ \forall\ i\ \lt j$, diagonal is also zeros $\to$ Forward Substitution  
- Upper Triangular, $a_{ij}\ =\ 0,\ \forall\ i\ \gt j$, diagonal is also zeros $\to$ Backward Substitution  
  
Julia syntax for solving Ax = b  
```  
A = rand(n,n)  
b = rand(n)  
  
x = A \ n  
```  
![[20240305_095212.jpg|600]]  
  
Forward Substitution: $x_i = {b_i - \sum_{j=1}^{i-1}a_{ij}x_j\over{a{ii}}}$  
  
```  
for i=1:n  
s = 0  
for j=1:i-1  
s = a[i,j] * x[j]  
end  
x[i] = (b[i] - s)/A[i,i]  
end  
```  
Backward Substitution:  
```  
for n:-1:1  
s = 0  
for j=i-1:-1:1  
s = A[i,j] * x[j]  
end  
x[i] = b[i] - s)A[i,j]  
end  
```  
  
If $A$ in $Ax = b$ is not triangular, factor with $A = LU \to LUx = b$  
1. $Ly=b \to y = L \div b$ forward $O(n^2)$  
2. $Ux = y \to x = U\div{b}$ backward $O(n^2)$  
  
Time Complexity Equation for loops: $\sum_{i=1}^n = {n(n+1)\over {2}}$  
  
[Master Theorem]([https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)):  
The Master Theorem provides a way to solve recurrence relations of the form:  
  
$$T(n) = aT({n\over {b}}) + f(n)$$  
  
where,  
  
- $T(n)$ is the time complexity of the algorithm,  
- $n$ is the size of the problem,  
- $a≥1a≥1$ is the number of subproblems into which the problem is divided,  
- $b>1b>1$ is the factor by which the subproblem size is reduced in each call,  
- $f(n)$ is the time complexity of the work done outside the recursive calls, including the division of the problem and the merging of results from subproblems.  
  
The theorem provides conditions under which the time complexity of the recurrence can be determined directly. It categorizes the solution based on the relationship between $f(n)$ and $n^{log⁡_ba}$, the critical part being how $f(n)$ compares to $n^{log⁡_ba}$.  
  
### The Master Theorem states that:  
  
1. **If $f(n)=O(n^c)$ where $c<log_⁡ba$, then $T(n)=Θ(n^log_⁡ba)$.**  
     
    This case applies when the cost of the recursive calls dominates the cost of the work done at each level.  
     
2. **If $f(n)=Θ(n^c)$ where $c=log⁡_ba$, then $T(n)=Θ(n^c log⁡ n)$.**  
     
    Here, the work done at each level of the recursion and the number of levels are balanced, contributing equally to the total complexity.  
     
3. **If f(n)=Ω(nc)f(n)=Ω(nc) where c>log⁡bac>logba and if af(nb)≤kf(n)af(bn)≤kf(n) for some constant k<1k<1 and sufficiently large nn, then T(n)=Θ(f(n))T(n)=Θ(f(n)).**  
     
    This condition applies when the work done outside the recursive calls dominates the total complexity.  
     
  
### Applications  
  
The Master Theorem is particularly useful in analyzing the time complexities of divide and conquer algorithms, where a problem is divided into smaller subproblems, each of a smaller size, which are then solved recursively, with some additional work done to split the problem and/or merge the solutions.  
  
### Example  
  
For the Merge Sort algorithm, the recurrence relation is:  
  
T(n)=2T(n2)+Θ(n)T(n)=2T(2n)+Θ(n)  
  
Here, a=2a=2, b=2b=2, and f(n)=Θ(n)f(n)=Θ(n). According to the Master Theorem, this falls into Case 2, since f(n)f(n) matches nlog⁡ba=nlog⁡22=nnlogba=nlog22=n. Thus, the time complexity of Merge Sort is T(n)=Θ(nlog⁡n)T(n)=Θ(nlogn).  
  
### Limitations  
  
The Master Theorem does not apply to all types of recurrence relations. For instance, it does not cover cases where the size of subproblems is not equal or when the rate of division is not constant. In such cases, other methods like the recursion tree method or the Akra-Bazzi method may be used to solve the recurrence.  
  
## 3/7/2024  
Coding Exercises:  
1. Generate random lower triangular matrix.  
1. Make use of definition of lower triangular  
2. generate "test" matricies  
2. "Is a" function to test if matrix *IS A* lower triangular.  
3. Using 1 and 2, generate 2 L.T's, then multiply $L_1\ \land\ L_2 \to L_1L_2, \to isLower(L_1\times L_2)$, product of matrices is closed    
  
Algebraic Props:  
- $a = b$  
- $c = d$  
- Therefor $a + c = b + d$  
- $a = b == ka = kb$  
- $k(a+c) = k(b+d)$  
- $ka + c = kb + d$  
  
- [Gaussian Elimination]([https://en.wikipedia.org/wiki/Gaussian_elimination](https://en.wikipedia.org/wiki/Gaussian_elimination)):  
- You can switch any 2 rows in a matrix  
- Multiply any row by a scalar  
- Add 2 rows and replace.  
  
Example:  
$$A = \begin{bmatrix} 1 & 4 &7 \\ 3 & 6 & 9 \\ 2 & 8 & 5\end{bmatrix} \to U.T.$$  
  
$R_2 = -3R_1 + R_2$  
$$A = \begin{bmatrix} 1 & 4 & 7 \\ 0 & -6 & -12 \\ 2 & 8 & 5\end{bmatrix}$$  
  
$R_3 = -2R_1 + R_3$ $$A = \begin{bmatrix} 1 & 4 & 7 \\ 0 & -6 & -12 \\ 0 & 0 & 5\end{bmatrix}$$  
  
L = by **Bookkeeping**  
$$\begin{bmatrix} 1 & 0 & 0 \\ 3 & 1 & 0 \\ 2 & 0 & 1\end{bmatrix}$$  
  
## 3/19/2024  
  
$$Ax = b \to L(Ux) = b$$  
Let $$Ux = y \to Ly=b$$solve using forward substitution for y.  
Then solve with backwards substitution. $$Ux = y$$for x.  
```  
JULIA CODE:  
using LinearAlgebra  
A = [-1 2 5; 2 -4 5; -1 0 5]  
# to get Lower and Upper triangle and Pivot Matrix  
(L, U, P) = lu(A)  
  
```  
## 3/21/2024  
  
Pivot Matrix (Partial Pivoting):  
```  
idx = i  
max = 0  
for k=j:n  
if A(k+1, j) > max:  
max = A[i+1][j]  
idx = k  
  
#####################  
Can also be done:  
argmax(abs(A[j:n,j])) + j  
  
```  
```  
A[:, j] --> the jth column  
A[j:n,j] --> the jth subcolumn  
```  
### Special Matrices:  
Have a structure we can exploit and take advantage of.  
- Banded matrix - mostly from differential equations  
$$\begin{bmatrix} -2 & 1 & 0 & 0 & 0 \\ 1 & -2 & 1 & 0 & 0 \\ 0 & 1 & -2 & 1 & 0 \\0 & 0 & 1 & -2 & 1 \\ 0 & 0 & 0 & 1 & -2\end{bmatrix}$$  
- Upper Bandwidth {q}  
$1 \le q \le n-1$  
$if\ a_{ij} = 0\ for\ j-i > q$  
q = 1  
- Lower Bandwidth {p}  
$1 \le p \le n-1$  
$if\ a_{ij} = 0\ for\ i-j > p$  
p = 1  
Bandwidth = p + q + 1 = 3 (aka 'w')  
$w \le 2n-1$  
- Symmetric Matrix (must be a square matrix): $A^T = A$  
$$\begin{bmatrix} 1 & 2 & 4 \\ 2 & 3 & 5 \\ 4 & 5 & 7\end{bmatrix}$$  
- Positive Definite Matrix: $x^TAx > 0 \iff PDM$  
- Most books will default to Symmetric Positive Definite Matrix  
- Show up in optimization Problems  
- Doesn't use LU factorization, uses Cholsky Factorization  
- Iterative Refinement:  
- James Wilkinson (Poppa of Numerical Analysis)  
- Goal: solve $Ax=b$  
1. $x_0 \approx x$  
2. compute the residual $b -Ax_0 = r_0$  
3. while not converged ($r \gt tolerance$)  
4. solve $Ac = r_i$  
1. $r_{i+1} = r_i -Ac_i$  
2. $x_i = x_i + c_i$  
  
## 3/26/2024  
# Recap  
## Goal:  
Solve $Ax = b \text{ where } A \in \mathbb{R}^{n \times n}$ - Factoring $A$ into $L$ and $U$ - Sometimes factor into $PA = LU \rightarrow LUx=PB$ - Use forward and backward substitution ## Special Matrices If $A$ was "special," then we can take advantage of special structures of $A$ - Banded - Symmetric - Definite - Positive Definite $\quad x^\mathsf{T}Ax > 0$ - Positive semidefinite $\quad x^\mathsf{T}Ax \ge 0$ - Negative Definite $\quad x^\mathsf{T}Ax < 0$ - Negative Semidefinite $\quad x^\mathsf{T}Ax \le 0$ ## Iterative Refinement ### Idea 1. start with initial approximation, $x_0$ 2. Improve (refine) $x_0 \rightarrow x_1,\ x_1 = x_0 + c_0$ where $c_0$ is the correction value for $x_0$ ### Actual Process 1. Perform $LU$ decomposition - an $O(n^3)$ operation - In mixed precision, this is typically done with **low** precision for performance gain and energy savings 2. Approximate $x_0 = U^{-1}L^{-1}b$ - **Never compute the inverse of a matrix** - Use substitution - $L(Ux)=b$ $Ux = L \backslash b$ forward substitution $x = U \backslash (L \backslash b)$ backward substitution 3. Compute Residual - $r_0 = b - Ax_0$ - In mixed precision, this is typically done with **high** precision 4. Compute Correction Value - $LUc_0 = r_0$ $c_0 = U \backslash L \backslash r_0$ 5. Compute next iteration - $_1 = x_0 + c_0$ 6. Go to step 3 - repeat until a threshold condition is met: often based on the residual ![[Untitled Diagram.drawio 2.svg]]# New Stuff  
## Solve  
$Ax=b, A \in \mathbb{R}^{m \times n},\ x \in \mathbb{R}^{n},\ b \in \mathbb{R}^{m},\ m \ge n$ i.e., not square > Banks destroyed the American dream $Ax=b$ does not have a solution: more equations than unknowns - solve $\rightarrow$ find best solution: minimize the residual > Youthful dreams of humdrum insurance analysis ### Background 1. Inner Product $<x, y> = x^\mathsf{T}y$ 2. Orthogonal $<x, y> = 0 \implies x \perp y$ 3. $<x, y> = ||x||_2^2$ 4. $||x|| = 1 \implies x$ a unit vector 5. $X = \set{x_1, x_2, \cdots, x_n}$ is orthogonal if $x_i^\mathsf{T}x_j = 0,\ i \ne j$ 6. $X$ is an orthonormal set if $||x_i|| = 1,\ \forall x_i \in X$  
  
## 3/28/2024  
  
**NEW GOAL:** "Solve" $Ax=b$ Where $A\ \in R^{mxn}, b\ \in R^m$ and x is "best" solution  
  
- Note: No exact solution. "Best" solution for which $Ax \approx b$ "closest" in the least square sense  
- Minimum in the 2-norm.  
$min || b-Ax ||_2 \to$ cost/loss function  
- $x \in Vector\ Space\ =\ V(with\ algebraic\ props)$  
- Every finite space has a basis.  
Chem. Example:  
V = {H,O,C,K,....} "Basis" elements of all matter = V  
Can build:  
$H_2O$, $C_6H_{12}O_6$, etc...  
  
Linear Combination: $$V = {C_1X_1 + C_2X_2 + ... +C_nX_n}$$  
**Basis:** An **Independent spanning** set of vectors.  
  
**Spanning Set:** The set of vectors ${x_1,x_2,x_3,...,x_n}$ spans V if $\forall v \in V$ OR Every vector in V can be written as a linear combination of the vector in the set ${x_1, x_2,...,x_n}$  
**Standard Basis:** $\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}$, $\begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}$,$\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$ = $R^3$  
![[3D_Vector.svg.png|200]]  
[Gram-Schmidt Orthogonalization Algorithm (Process)]([https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process](https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process)) Pg. 145  
Given k vectors v $1 , … , v k$ ![{\displaystyle \mathbf {v} _{1},\ldots ,\mathbf {v} _{k}}]([https://wikimedia.org/api/rest_v1/media/math/render/svg/916a7303fbee0f437f7214458a0dd6de886fb53a](https://wikimedia.org/api/rest_v1/media/math/render/svg/916a7303fbee0f437f7214458a0dd6de886fb53a)) the Gram–Schmidt process defines the vectors u 1 , … , u k ![{\displaystyle \mathbf {u} _{1},\ldots ,\mathbf {u} _{k}}]([https://wikimedia.org/api/rest_v1/media/math/render/svg/9bbb786f13046e085458c34a87f3951f1808b8ca](https://wikimedia.org/api/rest_v1/media/math/render/svg/9bbb786f13046e085458c34a87f3951f1808b8ca)) as follows:  
  
u 1 = v 1 , e 1 = u 1 ‖ u 1 ‖ u 2 = v 2 − proj u 1 ⁡ ( v 2 ) , e 2 = u 2 ‖ u 2 ‖ u 3 = v 3 − proj u 1 ⁡ ( v 3 ) − proj u 2 ⁡ ( v 3 ) , e 3 = u 3 ‖ u 3 ‖ u 4 = v 4 − proj u 1 ⁡ ( v 4 ) − proj u 2 ⁡ ( v 4 ) − proj u 3 ⁡ ( v 4 ) , e 4 = u 4 ‖ u 4 ‖     ⋮     ⋮ u k = v k − ∑ j = 1 k − 1 proj u j ⁡ ( v k ) , e k = u k ‖ u k ‖ .  
  
![{\displaystyle {\begin{aligned}\mathbf {u} _{1}&=\mathbf {v} _{1},&\!\mathbf {e} _{1}&={\frac {\mathbf {u} _{1}}{\|\mathbf {u} _{1}\|}}\\\mathbf {u} _{2}&=\mathbf {v} _{2}-\operatorname {proj} _{\mathbf {u} _{1}}(\mathbf {v} _{2}),&\!\mathbf {e} _{2}&={\frac {\mathbf {u} _{2}}{\|\mathbf {u} _{2}\|}}\\\mathbf {u} _{3}&=\mathbf {v} _{3}-\operatorname {proj} _{\mathbf {u} _{1}}(\mathbf {v} _{3})-\operatorname {proj} _{\mathbf {u} _{2}}(\mathbf {v} _{3}),&\!\mathbf {e} _{3}&={\frac {\mathbf {u} _{3}}{\|\mathbf {u} _{3}\|}}\\\mathbf {u} _{4}&=\mathbf {v} _{4}-\operatorname {proj} _{\mathbf {u} _{1}}(\mathbf {v} _{4})-\operatorname {proj} _{\mathbf {u} _{2}}(\mathbf {v} _{4})-\operatorname {proj} _{\mathbf {u} _{3}}(\mathbf {v} _{4}),&\!\mathbf {e} _{4}&={\mathbf {u} _{4} \over \|\mathbf {u} _{4}\|}\\&{}\ \ \vdots &&{}\ \ \vdots \\\mathbf {u} _{k}&=\mathbf {v} _{k}-\sum _{j=1}^{k-1}\operatorname {proj} _{\mathbf {u} _{j}}(\mathbf {v} _{k}),&\!\mathbf {e} _{k}&={\frac {\mathbf {u} _{k}}{\|\mathbf {u} _{k}\|}}.\end{aligned}}}|background-color:white]([https://wikimedia.org/api/rest_v1/media/math/render/svg/6ad89bad7c5fb0df82786c5b6938dce503af2dd0](https://wikimedia.org/api/rest_v1/media/math/render/svg/6ad89bad7c5fb0df82786c5b6938dce503af2dd0))  
Julia code:```  
function gramschmidt(V)  
   n, k = size(V)  
   U = zeros(n, k)  
   U[:, 1] = V[:, 1] / norm(V[:, 1])  
   for i in 2:k  
       U[:, i] = V[:, i]  
       for j in 1:i-1  
           U[:, i] = U[:, i] - (U[:, j]' * U[:, i]) * U[:, j]  
       end  
       U[:, i] = U[:, i] / norm(U[:, i])  
   end  
   return U  
end  
```  
  
## 4/2/2024  
[Orthogonality]([https://en.wikipedia.org/wiki/Orthogonality_(mathematics)](https://en.wikipedia.org/wiki/Orthogonality_(mathematics))): Metric of how correlated x and y are.  
$x \bot y \iff x^Ty=0$  
- Length of a vector is the sqrt of it's inner product  
$||x||_2 = \sqrt{<x,x>}$  
- i.e Euclidian Norm: $<x,x> = \sum^n_{i=1} x_i \dot x_i \to \sum^n_{i=1} x_i^2 \to \sqrt{\sum^n_{i=1} x_i^2}$  
  
Orthogonalization process:  
- $A = QU$ where Q is an orthogonal matrix and U is an Upper Triangular Matrix  
  
A is a rectangular matrix (can be a square matrix) of shape $R^{mxn}$  
A = $\{a_1, a_2,...,a_n\} \to$ set of vectors  
Q = $\{q_1, q_2,...,q_n\} \to$ set of vectors  
  
project $a_2$ on to $a_1$ to get $p$  
shift $a_2$ to be perpendicular to $a_1$ by using $a_1 - p$  
normalize  
  
U[5,7] = $q_5^Ta_7$  
  
A = $\begin{bmatrix} 1 & -1 & 4 \\ 1 & 4 & -2 \\ 1 & 4 & 2 \\ 1 & -1 & 0\end{bmatrix}$  
$[1,1,1,1]\begin{bmatrix} 4 \\ -2 \\ 2 \\ 0\end{bmatrix} = 4 +(-2)+2+0 = 4 \to 4 \ne 0 \to$ Matrix is orthogonal

  

|   |   |
|---|---|
|![](https://lh3.googleusercontent.com/a/ACg8ocIbBpsvJLAPDvjL7HFClnb4I6bm2ATyi5VUAyNh5RiLFepcArc=s40-p)||

|   |
|---|
||