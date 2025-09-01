// valve_control.cpp - التحكم بالصمامات
#include "valve_control.h"

void initValves(int pins[], int count) {
  for (int i = 0; i < count; i++) {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }
}

void controlValve(int valveNum, bool state, int pins[]) {
  if (valveNum < 0 || valveNum > 2) return;
  digitalWrite(pins[valveNum], state ? HIGH : LOW);
}