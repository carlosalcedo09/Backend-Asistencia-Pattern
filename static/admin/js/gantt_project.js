class Gantt {

    constructor(tasks) { 
      this.tasks = tasks;
      this.dateWidth = 178;
      this.setMinAndMaxDate(); 
      document.getElementById('gantt').innerHTML = this.buildTableHeader() + this.buildTableBody();
    }
  
    setMinAndMaxDate(){
      var maxDates = [];
      var minDates = [];
  
      for(let i = 0; i < this.tasks.length; i++){
        minDates.push(new Date(this.tasks[i][1]));
        maxDates.push(new Date(this.tasks[i][2]));     
      }
      this.minDate = new Date(Math.min.apply(null,minDates));
      this.maxDate = new Date(Math.max.apply(null,maxDates)); 
  
    }   

    getWeekNumber(d) {
      d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
      d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
      var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
      var weekNo = Math.ceil(((d - yearStart) / 86400000 + 1) / 7);
      return [d.getUTCFullYear(), weekNo];
    }

    buildTableHeader() {
      var html = '<table><thead><tr>';
      html += '<td class="first-column"></td>';
    
      var diffWeeks = this.diffInWeeks(this.maxDate, this.minDate) + 1;
      const actual = new Date(this.minDate);
    
      const today = new Date();
      today.setHours(0, 0, 0, 0);
    
      const [currentYear, currentWeekNumber] = this.getWeekNumber(today);
    
      for(let i = 0; i < diffWeeks; i++){
        let thClass = 'week';
        const [yearOfWeek, weekNumber] = this.getWeekNumber(new Date(actual));
    
        if(yearOfWeek < currentYear || (yearOfWeek === currentYear && weekNumber < currentWeekNumber)) {
          thClass = 'past-week';
        } else if (yearOfWeek === currentYear && weekNumber === currentWeekNumber) {
          thClass = 'current-week';
        }
    
        html += `<th class="${thClass}">` + actual.toISOString().substr(0, 10).replace('T', ' ') + "</th>";
        actual.setDate(actual.getDate() + 7);
      }
      html += '</tr></thead><tbody>';
      return html;
    }

    buildTableBody(){
      var html = '';
      for(let i = 0; i < this.tasks.length; i++){
        var task = this.tasks[i];
        var projectName = task[0]; 
        var dMin = new Date(task[1]);
        var dMax = new Date(task[2]);     
        var weeksBefore = this.diffInWeeks(dMin, this.minDate);
        var taskDurationInWeeks = this.diffInWeeks(dMax, dMin) + 1;
    
        html += '<tr>';
        html += `<td class="first-column">${projectName}</td>`;
        if(weeksBefore > 0) for(let j = 0; j < weeksBefore; j++) html += '<td></td>';
        html += '<td class="event-cell" colspan="'+ taskDurationInWeeks +'" style="background-color: '+task[3]+';"><span>'+task[4]+'% </span>'+task[0]+'</td>';
        html += '</tr>';
      }
      html += '</tbody></table>';
      return html;
    }

    diffInDays(max, min){
      var diffTime = Math.abs(max - min);
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
    }
  
    diffInWeeks(max, min){
      var diffTime = Math.abs(max - min);
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 7));
    }
  }