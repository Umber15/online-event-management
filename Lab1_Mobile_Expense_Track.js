let app=[{Day:"Monday",Expense:2000},
    {Day:"Tuesday",Expense:2500},
    {Day:"Wednesday",Expense:1500},
    {Day:"Thursday",Expense:200},
    {Day:"Friday",Expense:0},
    {Day:"Saturday",Expense:250},
    {Day:"Sunday",Expense:260},
]
console.log("---Mobile expense tracking app using for loop---")
for(let i=0;i<app.length;i++)
{
    console.log("The expense of "+ app[i].Day +" is "+ app[i].Expense)
}
let limit=0
for(let i=0;i<app.length;i++)
{
    if(app[i].Expense>2000)
      { limit++;}
}
console.log("---Count of days Expense exceed is---"+limit);
console.log("---Days in which limit exceeded---");
for(let i=0;i<app.length;i++)
{
    if(app[i].Expense>2000)
   {
     console.log("The expense of "+ app[i].Day +" is "+ app[i].Expense)
   }
}