library(ggplot2)
setwd('~/research/paper-drone2report/')

df = NULL


# LOADING DATA ------------------------------------------------------------
df_tmp = read.csv('results/cs4_optimizing_index/ms_train_val.csv')
df = rbind(df, 
               data.frame(
                 cycle = 1:nrow(df_tmp),
                 correlation = df_tmp$correlation_train,
                 set = 'train'
               ),
               data.frame(
                 cycle = 1:nrow(df_tmp),
                 correlation = df_tmp$correlation_val,
                 set = 'validation'
               )
)

# PLOT --------------------------------------------------------------------
p = ggplot(data = df, aes(x=cycle, y=correlation, color = set)) + 
  geom_line() + scale_color_manual(values=c('red', 'blue')) +
  xlab('Training iterations') + ylab('Correlation with\nheading date') + 
  geom_hline(yintercept = 0.109, colour = 'grey30', linewidth = 0.5, linetype = 3) + 
  geom_hline(yintercept = 0.135, colour = 'grey30', linewidth = 0.5, linetype = 3) +
  annotate('label', x=400, y=0.109, label = 'NDVI (multispectral)', color = 'grey30', hjust = 'right') +
  annotate('label', x=400, y=0.135,  label = 'GLI (RGB)', color = 'grey30', hjust = 'right') +
  theme_classic() + 
  theme(axis.title = element_text(face='bold', size = 18),
        axis.text = element_text(size = 15),
        legend.position = 'bottom')
print(p)
ggsave(
  filename = 'figures_tables/trajectories.png', 
  plot = p, width = 3000, height = 1800, units = 'px')

