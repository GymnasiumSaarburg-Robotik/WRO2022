# Data decryption

As described in the pixy porting guide the data from the Pixy BUS packet response can be interpreted after the following scheme

Example Data:
`[175, 193, 33, 14, 139, 2, 1, 0, 128, 0, 78, 0, 48, 0, 40, 0, 0, 0, 101, 255]`<br>

`[175, 193, 33, 28, 170, 5, 1, 0, 82, 0, 186, 0, 40, 0, 37, 0, 0, 0, 40, 255]
Following block: [1, 0, 160, 0, 185, 0, 40, 0, 36, 0, 0, 0, 132, 255]
`

`[175, 193, 33, 42, 82, 7, 1, 0, 252, 0, 191, 0, 36, 0, 29, 0, 0, 0, 2, 255]
[1, 0, 118, 0, 165, 0, 28, 0, 24, 0, 0, 0, 3, 255]
[1, 0, 6, 0, 22, 0, 12, 0, 18, 0, 0, 0, 200, 255]
`

`
[175, 193, 33, 56, 74, 5
21, 1, 195, 0, 38, 0, 22, 0, 0, 0, 17, 255]
14, 0, 22, 0, 28, 0, 21, 0, 0, 0, 18, 255, 
47, 1, 16, 0][26, 0, 20, 0, 0, 0, 117, 48, 
8, 0, 6, 0, 16, 0, 3, 0, 0, 0][135, 0
Valid: False

`

Response head:
`[175, 193, 33, 14, checksum x 2, colorcode x 2]`

Hier: `[175, 193, 33, 14, 139, 2, 1, 0]`

Remaining: `[128, 0, 78, 0, 48, 0, 40, 0, 0, 0, 101, 255]`

0 0-1  x-center | 0-315
Hier: `[128, 0]`

1 2-3  y-center | 0-207
Hier: `[78, 0]`

2 4-5  width / x | 0-316
Hier: `[48, 0]`

3 6-7  height / y | 0-208
Hier: `[40, 0]`


Remaining:
`[0, 0, 101, 255]`
`[Angle x 2, Tracking index, Age]`