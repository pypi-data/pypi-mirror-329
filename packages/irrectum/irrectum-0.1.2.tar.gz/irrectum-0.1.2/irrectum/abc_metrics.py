from abc import ABCMeta, abstractmethod
from typing import Union, Optional

import numpy as np


class Metric(metaclass=ABCMeta):

    @abstractmethod
    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, test_input: list = None, W: dict = None,
             lab_mse: float = None) -> Union[None, float, int]:
        pass


class RMSE(Metric):
    """
    Root-mean-squared-error - an assessment of the model's prediction error relative to the
    actual value y (Standard Deviation of Errors).
    A commonly used metric for evaluating the model's prediction error relative to the actual
    value y. For unbiased models, it coincides with the Standard Deviation of Errors. The smaller
    the value, the lower the model's error. It is free from the shortcomings of the
    Standard Deviation of Errors. A downside is that it cannot be used to compare quantities of
    different dimensions. It literally represents the square root of the average of the squared
    differences between the measured values and the mean. The smaller the Standard Deviation of
    Errors, the less variability there is in the quantity. A problem arises when samples have a
    good correlation but are far apart, as it will yield a good Standard Deviation of Errors due
    to the subtraction of the mean.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> float:
        """
        Root-mean-sqared-error

        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(RMSE)
            :param **kwargs:
        """
        try:
            ret = np.linalg.norm(np.subtract(
                test_target, test_prediction)) / np.sqrt(
                np.max([len(test_target), len(test_prediction)]))
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class NRMSE(RMSE):
    """
    Normalized Root Mean Squared Error - a normalized assessment of the
    model's prediction error relative to the actual value y (normalized
    Standard Deviation of Errors) RMSE, which is additionally divided by
    the total volatility of the sample (ymax - ymin). NRMSE lies in the
    range [0, 1]; the smaller the value, the lower the model's error.
    A modified version of NRMSE is used as a standard evaluation function
    in MATLAB: Fit = 100*(1 - NRMSE),
    which has the following interpretation: the percentage of agreement
    between the model and the original. Fit lies in the range [0, 100];
    the larger the value, the "closer" the model is to the original.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(NRMSE)
            :param **kwargs:
        """
        try:
            ret = super().test(test_target, test_prediction) / (
                    np.max([test_target, test_prediction]) -
                    np.min([test_target, test_prediction]))
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class Corr(Metric):
    """
    Pearson's linear correlation coefficient. The correlation coefficient
    varies between minus one and plus one. In our case, the closer the
    correlation coefficient is to 1, the better the trends of the two
    samples match. However, since the means are subtracted from the
    samples, there can be cases where the values perfectly match in trends
    with a correlation coefficient of 1 but are distant from each other by
    some value. In such cases, the root mean squared error is additionally
    provided.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(NRMSE)
            :param **kwargs:
        """
        try:
            ret = np.corrcoef(test_target, test_prediction)[0, 1]
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class CovMetric(Metric):
    """
    Covariance. If the covariance is positive, then as the values of one
    random variable increase, the values of the second tend to increase as
    well; if the sign is negative, they tend to decrease. However, one
    cannot judge the strength of the relationship between the variables
    solely based on the absolute value of covariance, as the value of
    covariance depends on their variances.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(COV)
            :param **kwargs:
        """
        try:
            ret = np.correlate(test_target, test_prediction)[0]
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class CoefDet(Metric):
    """
    The coefficient of determination (R-squared) represents the proportion
    of variance in the dependent variable that is explained by the model
    being considered, i.e., by the explanatory variables. The closer the
    coefficient of determination is to one, the stronger the dependence.
    The main problem with using R-squared is that its value increases
    (never decreases) with the addition of new variables to the model,
    even if those variables have no relation to the dependent variable!
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(R2)
            :param **kwargs:
        """
        try:
            ret = 1 - np.sum(np.power(np.subtract(
                test_target, test_prediction), 2)) / np.sum(
                np.power(np.subtract(test_target, np.mean(test_target)), 2))
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class MCoefDet(CoefDet):
    """
    The adjusted coefficient of determination is used to compare models
    with different numbers of factors, allowing for the number of
    regressors (factors) to not influence the statistics of the coefficient
    of determination. It uses unbiased estimates of variances and imposes
    a penalty for additional included factors, where n is the number of
    observations and k is the number of parameters. This measure is always
    less than one; the closer it is to 1, the stronger the dependence.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, test_input: list,
             **kwargs) -> Union[None, float, int]:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
            test_input [list] - list of model regressors
        return:
            Any[float, int] (MR2)
            :param **kwargs:
        """
        try:
            if len(test_target) - len(test_input) == 0:
                ret = None
            else:
                ret = 1 - (1 - super().test(test_target, test_prediction)) * (
                        len(test_target) - 1) / (len(test_target) - len(test_input))
                if not np.isfinite(ret):
                    ret = None
        except Exception:
            ret = None
        return ret


class RSS(Metric):
    """
    RSS. Residual sum of squares (errors) (SSR, SSE) is the sum of squared
    errors. The smaller the value, the better.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> float:
        """
         args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(RSS)
            :param **kwargs:
        """
        try:
            ret = np.sum(np.power(np.subtract(test_target, test_prediction), 2))
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class MAPE(Metric):
    """
    MAPE (mean absolute percentage error) measures the percentage error
    of the model relative to the original. MAPE lies in the range [0, 1];
    the smaller the value, the lower the percentage error of the models.
    Conceptually, it is close to NRMSE.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(MAPE)
            :param **kwargs:
        """
        try:
            ret = np.sum(
                np.abs(
                    np.divide(np.subtract(test_target, test_prediction),
                              test_target))) / len(test_target)
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class MAE(Metric):
    """
    MAE (mean absolute error) is a measure of errors between paired observations
    expressing the same phenomenon. Examples of Y compared to X include comparisons
    of predicted and observed values, subsequent time and initial time, as well
    as one measurement method compared to an alternative measurement method.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, **kwargs) -> Optional[float]:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
        return:
            float(MAE)
            :param **kwargs:
        """
        try:
            ret = np.sum(np.abs(np.subtract(test_target,
                                            test_prediction))) / len(test_target)
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class AIC(Metric):
    """
    AIC. The Akaike Information Criterion is a model comparison criterion
    that evaluates the quality of models not only based on accuracy (the
    second term of the sum) but also on the number of parameters used k
    (the first term of the sum). The smaller the value, the better the
    model is chosen. The Akaike Information Criterion imposes penalties
    for using additional model parameters, allowing for the selection
    of a model that is not the most accurate but reaches a compromise
    between accuracy and complexity.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, test_input: list, **kwargs) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
            test_input [list] - list of model regressors
        return:
            float(AIC)
            :param **kwargs:
        """
        try:
            ret = 2 * len(test_input) + len(test_target) * np.log(
                np.sum(np.power(np.subtract(test_target, test_prediction), 2)))
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class BIC(Metric):
    """
    BIC. The Bayesian Information Criterion (SC. Schwarz Criterion) is the
    most common modification of the Akaike Information Criterion. It
    imposes a greater penalty for using additional parameters k. The smaller
    the value, the better the model is chosen.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, test_input: list, **kwargs) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
            test_input [list] - list of model regressors
        return:
            float(BIC)
            :param **kwargs:
        """
        try:
            ret = len(test_input) * np.log(
                len(test_target)) - len(test_target) * np.log(
                np.sum(np.power(np.subtract(test_target, test_prediction), 2)))
            if not np.isfinite(ret):
                ret = None
        except Exception:
            ret = None
        return ret


class IQI:
    """
    Integral Quality Index. The Integral Quality Index offers a system of weights that allows
    for the redistribution of the contributions of the components of the
    IPK based on the requirements for specific properties of the model.
    The VAK index is defined as the average of the weighted indices of
    statistical metrics. The range of values for the IPK is: 0 ≤ IPK ≤ 100.
    """

    def test(self, test_target: np.ndarray, test_prediction: np.ndarray, W: dict, lab_mse: float) -> float:
        """
        args:
            test_target [numpy.ndarray] - real value of y
            test_prediction [numpy.ndarray] - model values
            testInput [list] - list of model regressors
            W (dict): weighting factors to account for the contribution to the overall assessment from the indicators
                        mae, r and r2
            lab_mse (float): convergence of the method

        return:
            float: IQI
        """

        try:
            mae = MAE().test(test_target, test_prediction)
            r = Corr().test(test_target, test_prediction)
            coef_det = CoefDet().test(test_target, test_prediction)
            S_y = np.sqrt(np.sum(np.subtract(test_target, np.mean(test_target)) ** 2) / (len(test_target) - 1))
            if np.isfinite(S_y):
                if S_y > lab_mse:
                    Hmae = 2 * lab_mse
                    Lmae = lab_mse
                    Hr = 0.6
                    Lr = 0
                    Hcoef_det = 0.3
                    Lcoef_det = 0
                else:
                    Hmae = 2 * lab_mse
                    Lmae = lab_mse
                    Hr = 0
                    Lr = 0
                    Hcoef_det = 0
                    Lcoef_det = 0

                if mae <= Lmae:
                    Imae = 100
                elif mae >= Hmae:
                    Imae = 0
                else:
                    Imae = (Hmae - mae) / (Hmae - Lmae) * 100

                if r <= Lr:
                    Ir = 0
                elif r >= Hr:
                    Ir = 100
                else:
                    Ir = (r - Lr) / (Hr - Lr) * 100

                if coef_det <= Lcoef_det:
                    Icoef_det = 0
                elif coef_det >= Hcoef_det:
                    Icoef_det = 100
                else:
                    Icoef_det = (coef_det - Lcoef_det) / (Hcoef_det - Lcoef_det) * 100

                ret = (W['W_mae'] * Imae + W['W_r'] * Ir + W['W_r2'] * Icoef_det) / 3
                if not np.isfinite(ret):
                    ret = None
            else:
                ret = None
        except Exception:
            ret = None
        return ret
