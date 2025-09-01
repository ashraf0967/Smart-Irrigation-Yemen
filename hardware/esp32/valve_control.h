// valve_control.h
#ifndef VALVE_CONTROL_H
#define VALVE_CONTROL_H

void initValves(int pins[], int count);
void controlValve(int valveNum, bool state, int pins[]);

#endif