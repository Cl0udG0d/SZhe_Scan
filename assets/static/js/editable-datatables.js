/*
	Modified by abhishek gahlot to work with latest jquery 1.11

*/
function restoreRow ( oTable, nRow )
{
	var aData = oTable.fnGetData(nRow);
	var jqTds = $('>td', nRow);

	for ( var i=0, iLen=jqTds.length ; i<iLen ; i++ ) {
		oTable.fnUpdate( aData[i], nRow, i, false );
	}

	oTable.fnDraw();
}

function editRow ( oTable, nRow )
{
	var aData = oTable.fnGetData(nRow);
	var jqTds = $('>td', nRow);
	jqTds[0].innerHTML = '<input type="text" class="form-control input-sm" value="'+aData[0]+'">';
	jqTds[1].innerHTML = '<input type="text" class="form-control input-sm" value="'+aData[1]+'">';
	jqTds[2].innerHTML = '<input type="text" class="form-control input-sm" value="'+aData[2]+'">';
	jqTds[3].innerHTML = '<input type="text" class="form-control input-sm" value="'+aData[3]+'">';
	jqTds[4].innerHTML = '<input type="text" class="form-control input-sm" value="'+aData[4]+'">';
	jqTds[5].innerHTML = '<a class="edit" href="">Save</a>';
}

function saveRow ( oTable, nRow )
{
	var jqInputs = $('input', nRow);
	oTable.fnUpdate( jqInputs[0].value, nRow, 0, false );
	oTable.fnUpdate( jqInputs[1].value, nRow, 1, false );
	oTable.fnUpdate( jqInputs[2].value, nRow, 2, false );
	oTable.fnUpdate( jqInputs[3].value, nRow, 3, false );
	oTable.fnUpdate( jqInputs[4].value, nRow, 4, false );
	oTable.fnUpdate( '<a class="edit" href="">Edit</a>', nRow, 5, false );
	oTable.fnDraw();
}

	var oTable = $('.editable-datatable').dataTable({
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
	var nEditing = null;

	$('#new').click( function (e) {
		e.preventDefault();

		var aiNew = oTable.fnAddData( [ '', '', '', '', '',
			'<a class="edit" href="">Edit</a>', '<a class="delete" href="">Delete</a>' ] );
		var nRow = oTable.fnGetNodes( aiNew[0] );
		editRow( oTable, nRow );
		nEditing = nRow;
	} );

	$('.editable-datatable').on('click', ' a.delete',function (e) {
		e.preventDefault();

		var nRow = $(this).parents('tr')[0];
		oTable.fnDeleteRow( nRow );
	} );

	$('.editable-datatable').on('click',  'a.edit',function (e) {
		e.preventDefault();

		/* Get the row as a parent of the link that was clicked on */
		var nRow = $(this).parents('tr')[0];

		if ( nEditing !== null && nEditing != nRow ) {
			/* Currently editing - but not this row - restore the old before continuing to edit mode */
			restoreRow( oTable, nEditing );
			editRow( oTable, nRow );
			nEditing = nRow;
		}
		else if ( nEditing == nRow && this.innerHTML == "Save" ) {
			/* Editing this row and want to save it */
			saveRow( oTable, nEditing );
			nEditing = null;
			alert('Stuff added, do add some ajax to save server side changes.')
		}
		else {
			/* No edit in progress - let's start one */
			editRow( oTable, nRow );
			nEditing = nRow;
		}
	});

//This is for bootstrap compatibility , original libraries havent been modified.
$('.dataTables_filter input,.dataTables_length select').addClass('form-control');

