# CORDIC-Vyper
Implementation of CORDIC algorithm from HP-35 in Vyper

Using a rotation matrix against a vector given with the initial coordiantes $`x_0$ and $`y_0$ we can write the equation

A great video to understand the intuition behind this is this video by [3Blue1Brown](https://youtu.be/O85OWBJ2ayo)

```math
\begin{bmatrix}
x(\theta)\\
y(\theta)
\end{bmatrix}
=
\begin{bmatrix}
 \cos(\theta) -\sin(\theta)\\
\sin(\theta) \cos(\theta)
\end{bmatrix}
\times
\begin{bmatrix}
x_0\\ 
y_0 
\end{bmatrix}
```
  </br>  
<div align="center">
matrix multiplication of the rotation matrix gives:
</div>

$$x(\theta)=x_0\cos(\theta)-y_0sin(\theta)$$

$$y(\theta)=x_0\sin(\theta)+y_0cos(\theta)$$
  
  </br>    
<div align="center">
substituting to only have cosine or sine in the equation 
</div>

$$\sin=\tan \times \cos into $$

$$x(\theta)=x_0\cos(\theta)-y_0sin(\theta)$$

$$x(\theta)=x_0\cos(\theta)-y_0 \times (\tan(\theta) \times \cos(\theta))$$

$$\cos=\tan \times \sin into $$

$$y(\theta)=x_0\sin(\theta)+y_0cos(\theta)$$

$$y(\theta)=x_0 \times(\tan(\theta) \times \sin(\theta))+y_0cos(\theta)$$

  </br>    
<div align="center">
factor out the cosine
</div>

$$x(\theta)=\cos(\theta) \times (x_0 - y_0\tan(\theta))$$

$$y(\theta)=\cos(\theta) \times (y_0 + x_0\tan(\theta))$$

  </br>    
<div align="center">
divide the cosine from each side of the =
</div>

$$\frac{x(\theta)}{\cos(\theta)} = x_0 - y_0\tan(\theta)$$

$$\frac{y(\theta)}{\cos(\theta)} = y_0 + x_0\tan(\theta)$$

  </br>    
<div align="center">
let's remove the cosine from the left side of the equation. It's a constant variable that we can multiply by x(t) and y(t) at the end 
</div>

$$x(\theta) = x_0 - y_0\tan(\theta) Eq.1$$

$$y(\theta) = y_0 + x_0\tan(\theta) Eq.2$$


