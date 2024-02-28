$(document).ready(function() {
    const checkAll = $('#checkAll');
    const searchInput = $('#searchInput');
    const table = $('#myTable');
    const rows = $('#myTable tbody tr');
    const noResults = $('#noResults');
    const allSelected = $('#allSelected');
    const attendanceCheckboxes = $('.attendanceCheckbox');
  
    checkAll.change(function() {
      attendanceCheckboxes.prop('checked', checkAll.prop('checked'));
      updateAllSelectedMessage();
    });
  
    $('.attendanceCheckbox').change(function() {
      updateAllSelectedMessage();
    });
  
    $('#attendanceForm').submit(function(event) {
      event.preventDefault();
      updateAttendance();
    });
  
    function updateAttendance() {
      let formData = $('#attendanceForm').serialize();
      $.ajax({
        url: '/update_attendance/',
        type: 'POST',
        data: formData,
        dataType: 'json',
        success: function(response) {
          console.log(response.message);
        },
        error: function(xhr, errmsg, err) {
          console.log('Error updating attendance.');
        }
      });
    }
  
    function updateAllSelectedMessage() {
      let allChecked = true;
      $('.attendanceCheckbox').each(function() {
        if (!$(this).prop('checked')) {
          allChecked = false;
          return false; // Break out of loop
        }
      });
      if (allChecked) {
        $('#allSelected').show();
      } else {
        $('#allSelected').hide();
      }
    }
  });
  