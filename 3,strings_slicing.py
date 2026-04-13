a = "budwjdbdkjqw" # Every character has its own index on it, b=0, u=1, d=2, so on.  
sliced = a[1:6] # 6th character will be excluded
print(sliced)

# Skipping a character in a string,
b = "ksjgdfhegvd"
skipped = b[2:5:2] # 'jgdf' then skipped characters, j=0(printed), g=1(skipped), d=2(printed) 
print(skipped)

c = "hdgbfuyefhwedjehfuibf"
skippedC = c[2:10:3] # Result of '[2:10]' is 'gbfuyefh', the indices now,
# g=0, b=1, f=2,..h=7, so after printing 'g' the character on 3rd then 
# 6th then 9th then so on, will be printed and hence the result will be 'guf'.

print("New strings after skipping characters in c is: ", skippedC)
