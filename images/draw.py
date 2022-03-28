import pandas as pd
import csv
import matplotlib.pyplot as plt

#df = pd.read_csv('graph4.csv', encoding='utf8')
df = pd.read_csv('graph6.csv', encoding='utf8')
df.plot(x="ML tools", y=["dos", "buf.-overflow", "arbi.-code-ex.", "xss", "open-redir.", "symlink-attack"], kind="bar", width=0.8)
#ax = df.plot.bar(x='ML tools',y='Total vulnerabilities',color='gray',rot=0) 
#figsize
#ax.set(xlabel="ML tools")
plt.legend(fontsize=8)
plt.xlabel('ML tools', fontsize=8)
#plt.ylabel('ylabel', fontsize=6)
plt.xticks(fontsize=6.5,rotation=39)
plt.yticks(fontsize=7.5)
#plt.show()
plt.savefig('advisorydb_attack_distribution_per_tool.pdf',bbox_inches='tight')
