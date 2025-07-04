from numpy import exp, log, sqrt
from scipy.stats import norm

class BlackScholes:
    def __init__(
            self, 
            time_to_maturity:float,
            strike: float,
            current_price:float,
            volatility:float,
            interest_rate: float,
        ):
            self.time_to_maturity= time_to_maturity
            self.strike = strike
            self.current_price = current_price
            self.volatility = volatility
            self.interest_rate = interest_rate

    def run(
                self,
        ):
            time_to_maturity = self.time_to_maturity #t
            strike = self.strike #K
            current_price = self.current_price #St
            volatility = self.volatility #sigma
            interest_rates = self.interest_rate #r

            d1 = (
                    log(current_price/strike)+
                    (interest_rates + 0.5*volatility**0.2)*time_to_maturity
            )/(
                    volatility*sqrt(time_to_maturity)
            )
            
            d2 = d1 - volatility*sqrt(time_to_maturity)

            call_price = current_price * norm.cdf(d1) - (
                   strike * exp(-(interest_rates*time_to_maturity))*norm.cdf(d2)
            )

            put_price = (
                   strike * exp(-(interest_rates*time_to_maturity))*norm.cdf(-d2)-current_price*norm.cdf(-d1)
            )

            #Greeks
            #Delta
            self.call_delta = norm.cdf(d1)
            self.put_delta = 1 - norm.cdf(d1)

            #Gamma
            self.call_gamma = norm.pdf(d1)/(
                   strike*volatility*sqrt(time_to_maturity)
                )
            self.put_gamma = self.call_gamma

if __name__ == "__main__":
       time_to_maturity = 2
       strike = 90
       current_price = 100
       volatility = 0.2
       interest_rate = 0.05

       BS = BlackScholes(
            time_to_maturity=time_to_maturity,
            strike=strike,
            current_price=current_price,
            volatility=volatility,
            interest_rate=interest_rate
       )
       BS.run()