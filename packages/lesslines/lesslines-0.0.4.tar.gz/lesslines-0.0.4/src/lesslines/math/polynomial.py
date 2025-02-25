class Polynomial:
    def __init__(self, coefs : list[float]):
        """
        Initialize a polynomial with its coefficients.
        
        Args:
        -----
        coefs : list[float]
            Coefficients of the polynomial stored as a list.
        """
        self.coefs = coefs
    
    def __str__(self):
        """
        Return string representation of the polynomial.
        
        Returns:
        --------
        s : str
            String representation of the polynomial.
        """
        terms = []
        for i, c in enumerate(self.coefs):
            if c != 0:
                terms.append(f"{c}x^{i}")
        s = ' + '.join(terms)
        s = s.replace('x^0', '')
        s = s.replace('x^1 ', 'x ')
        s = s.replace('x^1', 'x')
        s = s.replace(' 1x', ' x')
        s = s.replace(' 1.0x', ' x')
        s = s.replace('-1x', '-x')
        s = s.replace(' + -', ' - ')
        return s
    
    def __call__(self, x):
        """
        Evaluate the polynomial at specific value of x.
        
        Args:
        -----
        x : float
            Value to be evaluated using the polynomial.
        
        Returns:
        --------
        y : float
            Value returned by the polynomial.
        """
        y = 0
        for i, c in enumerate(self.coefs):
            y += c * x**i
        return y
    
    def differentiate(self):
        """
        Calculate derivative of the polynomial.
        
        Returns:
        --------
        new_poly : Polynomial
            New instance of Polynomial.
        """
        new_coefs = []
        for i, c in enumerate(self.coefs[1:]):
            new_coefs.append(c * (i + 1))
        new_poly = Polynomial(new_coefs)
        return new_poly

    def integrate(self, c=0):
        """
        Calculate integral of the polynomial.
        
        Args:
        -----
        c : float, optional
            Integration constant. Defaults to 0.
        
        Returns:
        --------
        new_poly : Polynomial
            New instance of Polynomial.
        """
        new_coefs = [c]
        for i, c in enumerate(self.coefs):
            new_coefs.append(c / (i + 1))
        new_poly = Polynomial(new_coefs)
        return new_poly
    
    def __add__(self, other):
        """
        Override the + operator to add two polynomials.
        
        Returns:
        --------
        new_poly : Polynomial
            New instance of Polynomial.
        """
        len_s = len(self.coefs)
        len_o = len(other.coefs)
        if len_s < len_o:
            self.coefs = self.coefs + [0] * (len_o - len_s)
        elif len_s > len_o:
            other.coefs = other.coefs + [0] * (len_s - len_o)
        new_coefs = []
        for a, b in zip(self.coefs, other.coefs):
            new_coefs.append(a + b)
        new_poly = Polynomial(new_coefs)
        return new_poly
    
    def __sub__(self, other):
        """
        Override the - operator to substract two polynomials.
        
        Returns:
        --------
        new_poly : Polynomial
            New instance of Polynomial.
        """
        len_s = len(self.coefs)
        len_o = len(other.coefs)
        if len_s < len_o:
            self.coefs = self.coefs + [0] * (len_o - len_s)
        elif len_s > len_o:
            other.coefs = other.coefs + [0] * (len_s - len_o)
        new_coefs = []
        for a, b in zip(self.coefs, other.coefs):
            new_coefs.append(a - b)
        new_poly = Polynomial(new_coefs)
        return new_poly

    def __mul__(self, other):
        """
        Override the * operator to multiply two polynomials.
        
        Returns:
        --------
        new_poly : Polynomial
            New instance of Polynomial.
        """
        len_s = len(self.coefs)
        len_o = len(other.coefs)
        new_coefs = [0] * (len_s + len_o - 1)
        for i, a in enumerate(self.coefs):
            for j, b in enumerate(other.coefs):
                new_coefs[i + j] += a * b
        new_poly = Polynomial(new_coefs)
        return new_poly
    
    def evaluate(self, x : list[float]):
        """
        Evaluate the polynomial for some values of x.
        
        Args:
        -----
        x : list[float]
            Values of x to be evaluated with the polynomial.
        
        Returns:
        y : list[float]
            Values obtained from the polynomial.
        """
        y = []
        for xi in x:
            yi = self(xi)
            y.append(yi)
        return y
