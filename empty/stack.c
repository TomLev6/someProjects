#include "stack.h"
#include <stdio.h>

void stack_init(Stack* stack) {
    stack->top = -1;
}

int is_empty(Stack stack) {
    return stack.top == -1;
}

int is_full(Stack stack) {
    return stack.top == MAX_SIZE - 1;
}

void stack_push(Stack* stack, stackItem value) {
    if (is_full(*stack)) {
        printf("Stack is full. Cannot push %c.\n", value);
        return;
    }
    stack->arr[++stack->top] = value;
}

stackItem stack_pop(Stack* stack) {
    return stack->arr[stack->top--];
}

stackItem stack_top(Stack stack) {
    return stack.arr[stack.top];
}