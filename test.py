import pyupbit

access = "qsBHWvmgqXyvMHMheKov2egxwvoWT00TEa5kYW09"          # 본인 값으로 변경
secret = "Z47FcEu3kxvIhFEfKBvxiwQFCsvx6bWFa6XmThJu"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회