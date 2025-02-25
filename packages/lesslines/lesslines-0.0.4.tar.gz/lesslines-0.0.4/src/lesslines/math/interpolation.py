class Linear:
    def __init__(self, xx : list[float], yy : list[float]):
        """
        Initialize a piecewise linear interpolation.
        
        Args:
        -----
        xx : list[float]
            Values of x for interpolation stored as a list.
        yy : list[float]
            Values of y for interpolation stored as a list.
        """
        self.xx = xx
        self.yy = yy
        self.a , self.b = self._calculate_coefs()
    
    def _calculate_coefs(self):
        """
        Calculate linear coefficients for each range.
        
        Returns:
        --------
        a, b : tuple[list[float], list[float]]
            A tuple containing:
            - a: List of zeroth coefficients (intercepts),
            - b: List of first coefficients (slopes).
        """
        x = self.xx
        y = self.yy
        a = []
        b = []
        for i, (_, _) in enumerate(zip(x[:-1], y[:-1])):
            b.append((y[i+1] - y[i])/(x[i+1] - x[i]))
            a.append(y[i] - b[i] * x[i])
        return a, b
    
    def __str__(self):
        """
        Return string representation of the interpolation.
        
        Returns:
        --------
        s : str
            A string where each line represents a segment of the interpolation.
            Each segment includes:
            - (x1, x2): Range of x values.
            - a: Zeroth coefficient.
            - b: First coefficient.
        """
        segments = ['(x1, x2), a, b']
        for i in range(len(self.a)):
            x1 = f'{self.xx[i]:.3f}'
            x2 = f'{self.xx[i+1]:.3f}'
            a = f'{self.a[i]:.3f}'
            b = f'{self.b[i]:.3f}'
            segment = '(' + x1 +  ', ' + x2 + '), '
            segment += a + ', ' + b
            segments.append(segment)
        s = '\n'.join(segments)
        return s
    
    def get_coefs(self):
        """
        Return interpolation coefficients for all ranges.
        
        Returns:
        --------
        a, b : tuple[list[float], list[float]]
            A tuple containing:
            - a: List of zeroth coefficients (intercepts),
            - b: List of first coefficients (slopes).
        """
        return self.a, self.b
    
    def interpolate(self, x : list[float]):
        """
        Generate interpolated output from given input values.
        
        Args:
        -----
        x : list[float]
            Values of x.
        
        Returns:
        --------
        y : list[float]
            Values of predicted y.
        """
        y = []
        for i, xi in enumerate(x):
            for j in range(len(self.a)):
                if self.xx[j] <= xi < self.xx[j+1]:
                    yi = self.a[j] + self.b[j] * xi
                    y.append(yi)
                elif xi == self.xx[j+1] and i == len(x) - 1:
                    yi = self.a[j] + self.b[j] * xi
                    y.append(yi)
            if len(y) > len(x):
                y.pop()
        return y
