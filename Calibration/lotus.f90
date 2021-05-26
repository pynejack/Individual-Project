program tandem_NACA
  use fluidMod, only: fluid
  use bodyMod,  only: bodyUnion
  use mympiMod, only: init_mympi,mympi_end,mympi_rank
  use gridMod,  only: xg,composite
  use imageMod, only: display
  use geom_shape
  implicit none
!
! -- Define parameter and declare variables
  ! numerical parameters
  real,parameter     :: c = 2**6               ! number of cells along the chord
  real,parameter     :: m(3) = (/8*c,5*c,1./)  ! number of cells along each axis
  integer            :: b(3) = (/2,1,1/)       ! MPI blocks (product must equal n_procs)
  ! physical parameters
  real,parameter     :: U = 1, Re = 10**4, nu = U*c/Re, St = 0.4
  real,parameter     :: hamp = c, freq = St*U/(2*hamp), pamp = atan(pi*St)-pi/18.
  real,parameter     :: hamp2 = 1*hamp, freq2 = 1*freq, pamp2 = atan(pi*(2*hamp2*freq2/U))-pi/18
  real,parameter     :: spacing = 3*c, phase = 1.75*pi
  ! variables
  real :: force1(3),force2(3),moment1(3),moment2(3), power1, power2
  integer :: n(3), box(4) = (/-c,-3*c,12*c,6*c/)
  logical :: root, there = .false.
  type(fluid) :: flow
  type(bodyUnion) :: geoms
!
! -- Initialize MPI (if MPI is OFF, b is set to 1)
  call init_mympi(ndims=2,set_blocks=b)
  root = mympi_rank()==0
!
! -- Initialize domain size and placement
  n = composite(m/b, prnt=root) ! points per block
  call xg(1)%stretch(n(1)*b(1), -6*c, -0.4*c,   6*c, 10*c, h_max=10., prnt=root) ! x-grid
  call xg(2)%stretch(n(2)*b(2), -4*c, -2.1*c, 2.1*c,  4*c,            prnt=root) ! y-grid
!
! -- Initialize the two foils and their motion
  call geoms%add(naca(chord=c, thick=0.16, pivot=0.25) &  ! foil 1
                    .map.init_rigid(6,p).map.init_rigid(2,y))
  call geoms%add(naca(chord=c, thick=0.16, pivot=0.25) &  ! foil 2
                    .map.init_rigid(6,p2).map.init_rigid(2,y2) &
                    .map.init_rigid(1,x2))
!
! -- Initialize fluid
  call flow%init(n,geoms,V=(/U,0.,0./),nu=nu,exit=.true.)
  call display(flow%velocity%vorticity_Z(), 'out_vort', lim = 0.25, box=box)
!
! -- Time update loop
  do while (flow%time*freq<20.and..not.there)  ! run 20 cycles or until kill switch
    call geoms%update(flow%time) ! update the geometries
    call flow%update(geoms)      ! update the flow
  !
  ! -- Compute and print metrics to fort.9
    force1 = -geoms%bodies(1)%pforce(flow%pressure)    ! foil 1 x,y,z force
    force2 = -geoms%bodies(2)%pforce(flow%pressure)    ! foil 2 x,y,z force
    moment1 = -geoms%bodies(1)%pmoment(flow%pressure) ! foil 1 x,y,z moment
    moment2 = -geoms%bodies(2)%pmoment(flow%pressure) ! foil 2 x,y,z moment
    write(9,'(f10.4,f8.4,8e16.8)') flow%time*freq,flow%dt,  & ! time and time step
       force1(1:2)/(0.5*c*U**2),moment1(3)/(0.5*c**2*U**2), & ! C_X,C_Y,C_M
       geoms%bodies(1)%ppower(flow%pressure)/(0.5*c*U**3),  & ! C_P
       force2(1:2)/(0.5*c*U**2),moment2(3)/(0.5*c**2*U**2), & ! C_X,C_Y,C_M
       geoms%bodies(2)%ppower(flow%pressure)/(0.5*c*U**3)     ! C_P
    flush(9)
  !
  ! -- Print image of the vorticity 8 times a cycle
     if(mod(flow%time,1/(8*freq))<flow%dt) then
        print *,flow%time*freq,flow%dt ! CFL
        call display(flow%velocity%vorticity_Z(), 'out_vort', lim = 0.25, box=box)
     end if
     inquire(file='.kill', exist=there)

  end do
  call flow%write()
  call mympi_end()
contains

!foil 1 pitch motion
  real(8) pure function p(t)
    real(8),intent(in) :: t
    p = -pamp*cos(2*pi*t*freq)
  end function p

!foil 1 heave motion
  real(8) pure function y(t)
    real(8),intent(in) :: t
    y = hamp*sin(2*pi*t*freq)
  end function y

!foil 2 pitch motion
  real(8) pure function p2(t)
    real(8),intent(in) :: t
    p2 = -pamp2*cos(2*pi*t*freq2+phase)
  end function p2

!foil 2 plunging motion
  real(8) pure function y2(t)
    real(8),intent(in) :: t
    y2 = hamp2*sin(2*pi*t*freq2+phase)
  end function y2

!foil 2 x-spacing
  real(8) pure function x2(t)
    real(8),intent(in) :: t
    x2 = spacing
  end function x2

!NACA Geometry
type(set) function naca(chord,thick,pivot,alpha)
    real,intent(in) :: chord
    real,intent(in),optional :: thick,pivot,alpha
    type(model_info) :: info
    ! the geometry is a NACA0012 defined from x=2.85-5.58, so
    real :: thick0=0.12, edge=2.8538, chord0=2.7303
    real :: t=0.12,piv=0.5,a=0

    if(present(thick)) t = thick
    if(present(pivot)) piv = pivot
    if(present(alpha)) a = alpha*pi/180. !convert to rad

    info%file = 'naca_square.IGS'
    info%x = (/-edge-piv*chord0,-10.271,-18.87/)
    info%r = (/a,0.,0./)
    info%s = chord/chord0*(/1.,t/thick0,-1./)
    info%xmax(1) = chord
    info%n = (/chord,chord,1./)
    ! surface_debug = .true.
    model_fill = .false.
    eps = 2.0
    naca = model_init(info)
  end function naca

end program tandem_NACA


