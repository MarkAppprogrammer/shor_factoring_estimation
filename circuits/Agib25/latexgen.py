def generate_latex_table(rows):
   latex = []
   latex.append(r"\begin{table}[t]")
   latex.append(r"\resizebox{\linewidth}{!}{")
   latex.append(r"  \begin{tabular}{|c|c||c|c|c|c|c|}")
   latex.append(r"    \hline")
   latex.append(r"    \multicolumn{2}{|c||}{} & \multicolumn{5}{c|}{Parameters} \\")
   latex.append(r"    \hline")
   latex.append(r"    $n$ & $n_e$ & $w_e$ & $w_m$ & $c_{\text{sep}}$ & $c_{\text{pad}}$ & $d$ \\")
   latex.append(r"    \hline")

   for row in rows:
      formatted_row = " & ".join(str(item) for item in row) + r" \\"
      latex.append(f"    {formatted_row}")
      latex.append(r"    \hline")

   latex.append(r"  \end{tabular}")
   latex.append(r"}")
   latex.append(r"\caption{}")
   latex.append(r"\label{tbl:params}")
   latex.append(r"\end{table}")
   
   return "\n".join(latex)

data = [line.split(",") for line in open('C:\\Users\\shado\\OneDrive\\Desktop\\QuantumComputing\\Research\\circuits\\Shor1991\\Agib25\\params.csv')]

datarows = [
   
]

for row in data:
   datarow = []

   datarow.append(int(''.join(filter(str.isdigit, row[1]))))
   datarow.append(int(''.join(filter(str.isdigit, row[2]))))
   datarow.append(int(''.join(filter(str.isdigit, row[3]))))
   datarow.append(int(''.join(filter(str.isdigit, row[4]))))
   datarow.append(int(''.join(filter(str.isdigit, row[9]))))
   datarow.append(int(''.join(filter(str.isdigit, row[10]))))
   datarow.append(int(''.join(filter(str.isdigit, row[14]))))

   datarows.append(datarow)

print(generate_latex_table(datarows))