#config
infile = 'paper-drone2report/data/Fiorenzuola_RGB-GLI-HUE.xlsx'
target_index = c('GLI_mean', 'HUE_mean')
outfile = 'paper-drone2report/results/time_curves.png'
number_of_plotted_lines = 20
highlight_these_lines = c(157, 36)

# LIBRARIES ---------------------------------------------------------------
library("ggplot2")
library("ggpubr")
library("dplyr")
library("tidyr")
library("data.table")
library("gghighlight")

# SUPPORT FUNCTIONS -------------------------------------------------------
parse_dataset = function(x){
  x = gsub(x = x, pattern = '_F_RGB', replacement = '')
  year  = substr(x, start = 1, stop = 2)
  month = substr(x, start = 3, stop = 4)
  day   = substr(x, start = 5, stop = 6)
  return(paste(sep='', '20', year, '-', month, '-', day))
}

# ACTUAL SCRIPT -----------------------------------------------------------

#loading, keeping only useful columns
df <- readxl::read_xlsx(infile, sheet = 1)
# df = read.csv(infile, stringsAsFactors = FALSE) ## if you want to read a .csv file instead
df = df[,c('dataset', 'gid', target_index)]


#preparing data for the plot
df = pivot_longer(data=df, cols = all_of(target_index), names_to = 'index')
df$index = gsub(x=df$index, pattern = '_mean', replacement = '', fixed = TRUE)
df$dataset = parse_dataset(df$dataset)
df$gid = as.character(df$gid)


#subsetting to a number of lines that allows for a sensible plot
plotted_lines = unique(df$gid)[1:number_of_plotted_lines]
df= df[df$gid %in% plotted_lines,]

#the actual plot
p = ggplot(data=df, aes(x=dataset, y=value, group=gid, color=gid)) + 
  geom_line(linewidth = 1.5) + geom_point(size=3) + 
  facet_wrap(vars(index), scales = 'free_y') +
  gghighlight(gid %in% highlight_these_lines, calculate_per_facet = TRUE, use_direct_label = FALSE, unhighlighted_params = list(linewidth = 1, size=1)) +  
  theme_pubclean() + 
  theme(legend.position = 'none', 
        axis.text.x = element_text(angle = -90, vjust = 0.5, hjust = 0),
        axis.title = element_blank(), axis.text = element_text(color='black')
        )
p

#saving
ggsave(filename = outfile, plot = p, width = 12)
