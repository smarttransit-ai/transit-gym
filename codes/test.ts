begin
	TimeStart 10
	TimeEnd 100
	Network 'test.1'
	Additional 'test.2'
	OutputName 'test1.sumocfg'
	DumpName 'test.3'
 	RouteFileName "Bus.rou.xml"
		"INCLUDE"
		vehicle "1AltonPark_A_inbound"
	RouteFileName "Chattanooga_Daily_Trips.rou.xml"
		"ALL"
end