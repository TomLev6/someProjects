#pragma once
#ifndef STACK_H
#define STACK_H

#define MAX_SIZE 100
typedef char stackItem;
typedef struct {
    int arr[MAX_SIZE];
    char top;
} Stack;

void stack_init(Stack* stack);
int is_empty(Stack stack);
int is_full(Stack stack);
void stack_push(Stack* stack, stackItem value);
stackItem stack_pop(Stack* stack);
stackItem stack_top(Stack stack);

#endif // STACK_H