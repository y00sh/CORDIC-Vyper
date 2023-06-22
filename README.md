# CORDIC-Vyper
Implementation of CORDIC algorithm from HP-35 calculator in Vyper

Calculate the $`\sin(\theta)`$ and $`\cos(\theta)`$ when given an angle $`\theta`$

Using a rotation matrix against a vector given with the initial coordiantes $`x_0`$ and $`y_0`$ we can write the equation

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
let's remove the cosine from the equation, for now. It's a constant variable that we can multiply back in at the end to solve for 4x(t) and y(t) 
</div>

$$x(\theta) = x_0 - y_0\tan(\theta) Eq.1$$

$$y(\theta) = y_0 + x_0\tan(\theta) Eq.2$$

Now here is the magic of cordic we will, start with our initial unit vector described with the coordinates (1,0). When performing the vector rotation, the result is the final x and y coordinates of rotated vector. Trigonometric formualas tell us that:

<p align="center">
  <img width="200" alt="image" src="https://github.com/y00sh/CORDIC-Vyper/assets/90585099/1b7340da-21d6-4510-ad45-5e23ce2c4ebd">
</p>

$$\cos(\theta) = \frac{adj}{hyp}$$

$$\sin(\theta) = \frac{opp}{hyp}$$

But since its a unit vector hyp=1. Therefore the final x-coordinate is actually $`\cos(\theta)`$ since adj is the x-axis and the final y-coordinate is actually $`\sin(\theta)`$ since opp is the y-axis. Now to solve for sine and cosine we need to know the $`\theta`$ to rotate the vector in Eq 1 and 2. But those equations require calculating tangent and we are trying to solve for trigonometric functions, we dont have it yet, like asking for the chicken when we don't have the egg.  

The Eureka moment in solving this is to utilize a lookup table to replace $`\tan(\theta)`$ with the $`\theta`$ angles being in steps of $`2^{-n}`$.  

| $\alpha = \tan^{-1}(2^{-n})$ | $A=\tan(\alpha)$ |
| ------------------------ | -------------- |
| 45                       | 1              |
| 26.565                   | 0.5            |
| 14.036                   | 0.25           |
| 7.125                    | 0.125          |

So let's create a lookup table we can rewrite our Eq 1 and 2 and replace the $`\tan(\theta)`$ with $`2^{-n}`$

```python
A: decimal[34] = [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.00390625, 0.001953125, 0.0009765625, 0.0004882813, 0.0002441406, 0.0001220703, 0.0000610352, 0.0000305176, 0.0000152588, 0.0000076294, 0.0000038147, 0.0000019073, 0.0000009537, 0.0000004768, 0.0000002384, 0.0000001192, 0.0000000596, 0.0000000298, 0.0000000149, 0.0000000075, 0.0000000037, 0.0000000019, 0.0000000009, 0.0000000005, 0.0000000002, 0.0000000001] 
alpha: decimal[34] = [45.0, 26.5650511771, 14.0362434679, 7.125016349, 3.576334375, 1.7899106082, 0.8951737102, 0.4476141709, 0.2238105004, 0.1119056771, 0.0559528919, 0.0279764526, 0.0139882271, 0.0069941137, 0.0034970569, 0.0017485284, 0.0008742642, 0.0004371321, 0.0002185661, 0.000109283, 0.0000546415, 0.0000273208, 0.0000136604, 0.0000068302, 0.0000034151, 0.0000017075, 0.0000008538, 0.0000004269, 0.0000002134, 0.0000001067, 0.0000000534, 0.0000000267, 0.0000000133, 0.0000000067]
```

$$x(\theta) = x_0 - (y_0 \times r_n \times 2^{-n}) Eq.3$$

$$y(\theta) = y_0 + (x_0 \times r_n \times 2^{-n}) Eq.4$$

where $`r_n`$ determines whether the rotation of the unit vector is positive or negative. Lets use right-hand rule and if we are rotating the vector counterclockwise $`r_n=+1`$ and $`r_n = -1`$ if clockwise. We will push the unit vector in smaller and smaller steps until $`\theta`$ equals the angle that was given as an argument.

Let's go through an example where we would like to find $`\sin(55°)`$ or $`\cos(55°)`$
<table>
  <tr>
    <td align="center"><img src="https://github.com/y00sh/CORDIC-Vyper/assets/90585099/1751b50c-a430-4710-b88e-ae96264edfbc" width="200"><br>starts at 0°</td>
    <td align="center"><img src="https://github.com/y00sh/CORDIC-Vyper/assets/90585099/773004ac-80b0-4ddb-8767-c5d7be59c54b" width="200"><br>rotate ccw by 45°</td>
    <td align="center"><img src="https://github.com/y00sh/CORDIC-Vyper/assets/90585099/ed979d97-b6a5-495f-b7c2-3251cebb14f8" width="200"><br>rotate ccw by 26.565°</td>
    <td align="center"><img src="https://github.com/y00sh/CORDIC-Vyper/assets/90585099/28e9dd11-7bad-485f-93f4-13bd393e421b" width="200"><br>rotate cw by 14.036°</td>
    <td align="center"><img src="https://github.com/y00sh/CORDIC-Vyper/assets/90585099/b26989f3-92e7-4357-91e3-94c59a7dfd52" width="200"><br>rotate cw by 7.125°</td>
  </tr>
</table>

The blue unit vector is our target angle and the red unit vector is the vector that we are rotating. If the red vector is below the target angle we rotate it ccw on the next iteration. If the red vector exceeds the target angle we rotate it cw on the next iteration. We must keep track of the x and y coordinates during each iteration as the final values will (almost) be our answer

```python
    target_angle: decimal = angle % 90.0
    x: decimal = 1.0    # cosine 
    temp_x: decimal = 0.0  
    y: decimal = 0.0    # sine
    theta: decimal = 0.0  #degrees
    
    for i in range(35):  #35
        if theta < target_angle:
            temp_x = x - (y*A[i]) # since y needs the original x for the calc , too bad no more simultaneous assignment in vyper
            y = y + (x*A[i])
            x = temp_x
            theta = theta + alpha[i]
        else:
            temp_x = x + (y*A[i]) # since y needs the original x for the calc 
            y = y - (x*A[i])
            x = temp_x
            theta = theta - alpha[i]
```

We can also see that the target angle must be between 90° and 0°. If the angle exceeds this we can fold it due to the symmetry of sine and cosine. If it is 100° → 80°, 230° → 50°, 340° → 70°

```python
target_angle: decimal = angle % 90.0
```



We must also remember the $`\sin(\theta)`$ and $`\cos(\theta)`$ will be positive or negative based on which quadrant we are in. 

<p align="center">
  <img width="300" alt="image" src="https://github.com/y00sh/CORDIC-Vyper/assets/90585099/bc225c6b-656a-4ec3-a5e0-63ae00fd78e3">
</p>

```python
    if 0 <= angle < 90:
        # Quadrant I
        return x, y
    elif 90 <= angle < 180:
        # Quadrant II
        return -x, y"
    elif 180 <= angle < 270:
        # Quadrant III
        return -x, -y"
    else:
        # Quadrant IV
        return x, -y
```


