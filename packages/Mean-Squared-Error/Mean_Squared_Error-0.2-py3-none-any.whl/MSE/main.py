# x=Actual value, y=Predicted value
def MSE(x, y):
    try:  
        error=0       
        for i in range(len(x)):
            X=x[i]
            Y=y[i]
            error+=(X-Y)**2
        error=error/len(x)
        return error
    except:
        return "ERROR, CHECK THE INPUT VALUES"