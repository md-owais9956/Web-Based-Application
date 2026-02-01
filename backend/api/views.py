import pandas as pd
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# Global variable to store history in memory for the screening task
# In a full production app, you would save this to the SQLite database
upload_history = []

class AnalyzeCSVView(APIView):
    """
    Handles CSV upload, performs data analytics using Pandas, 
    and returns summary statistics for Web and Desktop clients.
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Read CSV using Pandas
            df = pd.read_csv(file_obj)

            # 2. Perform Analytics
            # Calculate Averages
            avg_pressure = float(df['Pressure'].mean())
            avg_flowrate = float(df['Flowrate'].mean())
            
            # Get Equipment Type Distribution (for Charts)
            type_dist = df['Type'].value_counts().to_dict()
            
            # Prepare Summary Data
            summary = {
                "equipment_name": file_obj.name,
                "total_count": len(df),
                "avg_pressure": round(avg_pressure, 2),
                "avg_flowrate": round(avg_flowrate, 2),
                "type_distribution": type_dist,
                "data_preview": df.to_dict(orient='records')
            }

            # 3. History Management
            # Add to the beginning of the list and keep only the last 5
            upload_history.insert(0, summary)
            if len(upload_history) > 5:
                upload_history.pop()

            return Response(summary, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Failed to process file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(APIView):
    """
    Returns the last 5 uploaded datasets with their summaries.
    """
    def get(self, request):
        return Response(upload_history, status=status.HTTP_200_OK)

class ExportPDFView(APIView):
    """
    Generates a basic PDF report for the most recent analysis.
    """
    def get(self, request):
        if not upload_history:
            return Response({"error": "No data available to generate report"}, status=status.HTTP_400_BAD_REQUEST)
        
        latest = upload_history[0]
        
        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Equipment_Report.pdf"'
        
        # Draw on PDF
        p = canvas.Canvas(response)
        p.setTitle("Chemical Equipment Report")
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "Chemical Equipment Parameter Report")
        
        p.setFont("Helvetica", 12)
        p.drawString(100, 770, f"File Analyzed: {latest['equipment_name']}")
        p.drawString(100, 750, f"Total Equipment: {latest['total_count']}")
        p.drawString(100, 730, f"Average Pressure: {latest['avg_pressure']} bar")
        p.drawString(100, 710, f"Average Flowrate: {latest['avg_flowrate']} m3/h")
        
        p.drawString(100, 680, "Equipment Distribution:")
        y_pos = 660
        for eq_type, count in latest['type_distribution'].items():
            p.drawString(120, y_pos, f"- {eq_type}: {count}")
            y_pos -= 20
            
        p.showPage()
        p.save()
        return response