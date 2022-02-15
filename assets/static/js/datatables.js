	//Simple datatable with no tabletools defined
	$('#simpledatatable').dataTable({
				"sDom": 'T<"clear">lfrtip',
				"sPaginationType": "bootstrap",
				"oLanguage": {
					"sLengthMenu": "_MENU_ records per page"
				},
				"oTableTools": {
					"sSwfPath": "lib/datatables/TableTools/swf/copy_csv_xls_pdf.swf",
					}
            });

	$('#advancetable').dataTable({
				"sDom": 'T<"clear">lfrtip',
				"sPaginationType": "bootstrap",
				"oLanguage": {
					"sLengthMenu": "_MENU_ records per page"
				},
				"oTableTools": {
					"sSwfPath": "lib/datatables/TableTools/swf/copy_csv_xls_pdf.swf",
					"aButtons": [
						{
							"sExtends":    "collection",
							"sButtonText": 'Tools <span class="caret" />',
							"aButtons":    [ "copy","csv", "xls", "pdf","print" ]
						}
					]
				}
            });


//Expanding tables code
function fnFormatDetails ( oTable, nTr )
{
	var aData = oTable.fnGetData( nTr );
	var sOut = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:10px;">';
	sOut += '<tr><td>Rendering engine:</td><td> '+aData[1]+' '+aData[4]+'</td></tr>';
	sOut += '<tr><td>Link to source: </td><td>Could provide a link here</td></tr>';
	sOut += '<tr><td>Extra info: </td><td>And any further details here (images etc)</td></tr>';
	sOut += '</table>';

	return sOut;
}

	/*
	 * Insert a 'details' column to the table
	 */
	var nCloneTh = document.createElement( 'th' );
	var nCloneTd = document.createElement( 'td' );
	nCloneTd.className = "center";

	$('#expandingtables thead tr').each( function () {
		this.insertBefore( nCloneTh, this.childNodes[0] );
	} );

	$('#expandingtables tbody tr').each( function () {
		this.insertBefore(  nCloneTd.cloneNode( true ), this.childNodes[0] );
	} );

	/*
	 * Initialse DataTables, with no sorting on the 'details' column
	 */
	var oTable = $('#expandingtables').dataTable( {
		"aoColumnDefs": [
			{ "bSortable": false, "aTargets": [ 0 ] }
		],
		"aaSorting": [[1, 'asc']]
	});

	/* Add event listener for opening and closing details
	 * Note that the indicator for showing which row is open is not controlled by DataTables,
	 * rather it is done here
	 */


//Expanding tables code end


//This is for bootstrap compatibility , original libraries havent been modified.
$('.dataTables_filter input,.dataTables_length select').addClass('form-control');
