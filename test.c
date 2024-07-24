#include<stdio.h>
int add(int arr[],int first, int max,int min){
  if(first<10){
     scanf("%d",&arr[first]);
    if(arr[first] >=max){
      max = arr[first];
    }
    if(arr[first] <=min){
      min = arr[first];
    }
  }
  else if(first ==10){
    printf("Maximum = %d\nMinimum = %d\n",max,min);
    return 0;
  }
  add(arr,first+1,max,min);

}
int main(){
int arr[10];
add(arr,0,arr[0],arr[0]);
return 0;}
