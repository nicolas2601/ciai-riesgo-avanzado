# Análisis crítico del benchmark supervisado

Modelo seleccionado en validación: **E_rf_balanced** (macro-F1 val 0.5933). Test confirma una sola vez, sin re-selección.

## 1. Baseline sin aprendizaje
A_dummy_majority en validación: macro-F1 0.3249, balanced accuracy 0.3333, accuracy 0.9505. Predice siempre la clase baja; su accuracy alta solo refleja el desbalance.

## 2. Mejora del modelo ponderado
B_logreg_balanced en validación: macro-F1 0.5253 (delta +0.2004 vs dummy).

## 3. SMOTE en validación
D_smote_logreg: macro-F1 0.5367 (B: 0.5253, delta +0.0114), balanced accuracy 0.6914 (B: 0.6759). SMOTE mejora en validación; falta confirmar en test.

## 4. Clase medio (precisión/recall)
Validación E_rf_balanced: precisión 0.2222, recall 0.0571, F1 0.0909, soporte 35. Dummy: precisión 0.0, recall 0.0, F1 0.0, soporte 35.

## 4. Clase alto (precisión/recall)
Validación E_rf_balanced: precisión 0.6296, recall 0.8095, F1 0.7083, soporte 21. Dummy: precisión 0.0, recall 0.0, F1 0.0, soporte 21.

## 5. Sobreajuste y degradación temporal
E_rf_balanced val macro-F1 0.5933 vs test 0.5296 (delta -0.0637). Sin métricas de entrenamiento no se afirma sobreajuste clásico; la comparación val->test mide degradación temporal.
- medio: recall val 0.0571 (n=35) vs test 0.0 (n=41).
- alto: recall val 0.8095 (n=21) vs test 0.7368 (n=19).

## 6. Estabilidad de la clase alta
Soportes: val 21, test 19. Con decenas de ejemplos, cada acierto/error mueve el recall en puntos; las métricas de clase alta son orientativas, no estables.

## 7. La mejora se mantiene en test
E_rf_balanced test macro-F1 0.5296 vs dummy test 0.3255 (delta +0.2041).

## 8. Límites para uso operativo
- El modelo clasifica actividad municipal del mes siguiente; NO predice cuándo ocurrirá un terremoto.
- No estima daños, ni produce probabilidades oficiales de amenaza, ni demuestra reducción de pérdidas.
- El catálogo SGC es retrospectivo/revisado: backtest, no operación as-of.
- La población DANE es proyección retrospectiva CNPV2018.
- La clase alta tiene soporte mínimo; cualquier despliegue requeriría validación, incertidumbre y revisión de Zabdiel.
