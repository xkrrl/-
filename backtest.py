import pyupbit
import numpy as np

# OHLCV(Open, High, Low, Close, Volume)으로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
#count 7이므로 7일간의 데이터로 백테스팅 할것임. 변경가능.
df = pyupbit.get_ohlcv("KRW-BTC", count=7)

#<전략>
#  
# 변동폭 * k 계산, (고가 - 저가) * k값. 지금은 0.5가 k값
df['range'] = (df['high'] - df['low']) * 0.5
#target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
#open(시가)에 위에서 구한 range값을 더해주고 한칸 내리기 위하여 shift로 1만큼 내려줌. 
#그렇게 시가에서 범위값을 더한 매수가(target)을 구할 수 있게됨.
df['target'] = df['open'] + df['range'].shift(1)
#</전략>

#ror(수익률), np(=Nunpy).where(조건문, 참일때 값, 거짓일때 값)
#여기서 조건문은 high 즉 고가가 target보다 높으면(참이면) close종가일때 target를 모두 매도하기때문에
#수익률은 close/target이 된다. 
#하지만 조건문이 거짓이면 (고가가 target보다 낮으면)매수 자체를 진행하지 않으므로 수익률은 1이다.
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)

#수익률을 누적해서 곱하여 계산(cumprod). 즉 누적 수익률이 된다.
df['hpr'] = df['ror'].cumprod()

#하락폭(Draw Down)을 계산해 주기 위해서 (누적 최대값과 현재 hpr차이 / 누적 최대값 * 100) 을 계산함.
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#Draw Down중 가장 큰 Max값. MDD=Max Draw Down
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")