::隔600s无限循环
for /l %%i in (1,0,1000) do (python ./QueryMail.py & TIMEOUT /T 600)
