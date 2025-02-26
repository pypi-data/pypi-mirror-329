PROGRAM mixed_precision
  USE mixed_precision_psy, ONLY: invoke_0
  USE constants_mod, ONLY: r_def, r_solver, r_tran, r_bl, r_phys
  USE field_mod, ONLY: field_type
  USE r_solver_field_mod, ONLY: r_solver_field_type
  USE r_tran_field_mod, ONLY: r_tran_field_type
  USE r_bl_field_mod, ONLY: r_bl_field_type
  USE r_phys_field_mod, ONLY: r_phys_field_type
  USE operator_mod, ONLY: operator_type
  USE r_solver_operator_mod, ONLY: r_solver_operator_type
  USE r_tran_operator_mod, ONLY: r_tran_operator_type
  REAL(KIND = r_def) :: scalar_r_def
  REAL(KIND = r_solver) :: scalar_r_solver
  REAL(KIND = r_tran) :: scalar_r_tran
  REAL(KIND = r_bl) :: scalar_r_bl
  REAL(KIND = r_phys) :: scalar_r_phys
  TYPE(field_type) :: field_r_def
  TYPE(r_solver_field_type) :: field_r_solver
  TYPE(r_tran_field_type) :: field_r_tran
  TYPE(r_bl_field_type) :: field_r_bl
  TYPE(r_phys_field_type) :: field_r_phys
  TYPE(operator_type) :: operator_r_def
  TYPE(r_solver_operator_type) :: operator_r_solver
  TYPE(r_tran_operator_type) :: operator_r_tran
  CALL invoke_0(scalar_r_def, field_r_def, operator_r_def, scalar_r_solver, field_r_solver, operator_r_solver, scalar_r_tran, &
&field_r_tran, operator_r_tran, scalar_r_bl, field_r_bl, scalar_r_phys, field_r_phys)
END PROGRAM mixed_precision