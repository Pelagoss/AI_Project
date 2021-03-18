setlocal enableextensions enabledelayedexpansion
set /a count=0
for %%f in (*.wav) do (
    ren "%%f" sample_!count!.wav
	set /a count+=1
)